"""
晶体学知识库检索模块
支持关键词搜索、分类过滤、语义关联检索
"""
import json
import os
import re

KB_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(KB_DIR, "kb_index.json")


class KnowledgeBase:
    def __init__(self):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            self.index = json.load(f)
        self._cache = {}  # category filename -> entries

    def _load_category(self, category_file):
        if category_file not in self._cache:
            filepath = os.path.join(KB_DIR, category_file)
            with open(filepath, "r", encoding="utf-8") as f:
                self._cache[category_file] = json.load(f)
        return self._cache[category_file]

    def search(self, query, top_k=5):
        """
        关键词搜索。
        query: 中文或英文搜索词
        top_k: 返回最相关的结果数
        """
        query_lower = query.lower()
        scores = {}

        for entry_id, meta in self.index.items():
            score = 0
            zh_title = meta["title_zh"].lower()
            en_title = meta["title_en"].lower()
            # 标题双向匹配
            if query_lower in zh_title or zh_title in query_lower:
                score += 10
            if query_lower in en_title or en_title in query_lower:
                score += 8
            # 标签双向匹配
            for tag in meta["tags"]:
                tag_lower = tag.lower()
                if tag_lower in query_lower or query_lower in tag_lower:
                    score += 5
            # 分类匹配
            if query_lower in meta["category"]:
                score += 3

            if score > 0:
                scores[entry_id] = score

        # 按分数排序
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        seen_categories = set()

        for entry_id, score in ranked[:top_k * 2]:
            meta = self.index[entry_id]
            entries = self._load_category(meta["file"])
            for entry in entries:
                if entry["id"] == entry_id:
                    results.append({**entry, "score": score})
                    seen_categories.add(meta["file"])
                    break
            if len(results) >= top_k:
                break

        return results[:top_k]

    def get_by_id(self, entry_id):
        """按 ID 精确获取"""
        if entry_id not in self.index:
            return None
        meta = self.index[entry_id]
        entries = self._load_category(meta["file"])
        for entry in entries:
            if entry["id"] == entry_id:
                return entry
        return None

    def get_related(self, entry_id):
        """获取关联条目"""
        entry = self.get_by_id(entry_id)
        if not entry:
            return []
        related = []
        for rid in entry.get("related", []):
            r = self.get_by_id(rid)
            if r:
                related.append(r)
        return related

    def list_by_category(self, category):
        """按分类列出"""
        cat_file = f"categories/{category}.json"
        if cat_file not in self._cache:
            filepath = os.path.join(KB_DIR, cat_file)
            if not os.path.exists(filepath):
                return []
            with open(filepath, "r", encoding="utf-8") as f:
                self._cache[cat_file] = json.load(f)
        return self._cache[cat_file]

    def format_for_llm(self, entry, include_related=True):
        """格式化为适合发给 LLM 的文本"""
        lines = [
            f"## {entry['title_zh']} ({entry['title_en']})",
            f"分类: {entry['category']} | 难度: {entry.get('difficulty', 'N/A')}",
            f"标签: {', '.join(entry.get('tags', []))}",
            f"来源: {entry.get('source', 'N/A')}",
            "",
            entry["content"],
        ]
        if entry.get("formulas"):
            lines.append(f"\n关键公式: {', '.join(entry['formulas'])}")

        if include_related and entry.get("related"):
            related_titles = []
            for rid in entry["related"]:
                if rid in self.index:
                    related_titles.append(self.index[rid]["title_zh"])
            if related_titles:
                lines.append(f"\n相关概念: {', '.join(related_titles)}")

        return "\n".join(lines)


# ============================================================
# 简单测试
# ============================================================
if __name__ == "__main__":
    kb = KnowledgeBase()
    print(f"Loaded {len(kb.index)} entries\n")

    # 测试搜索
    queries = ["布拉格", "NaCl", "位错", "能带", "Bragg", "Miller"]
    for q in queries:
        results = kb.search(q, top_k=2)
        print(f"搜索 '{q}':")
        for r in results:
            print(f"  [{r['score']}] {r['title_zh']}")
        print()
