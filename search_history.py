# audit/search_history.py
import os
import json
from datetime import datetime

class SearchHistory:
    """Tracks user search history — save, retrieve, stats"""

    def __init__(self, history_file="audit/search_history.json"):
        self.history_file = history_file
        self.history = {}               # {user: [{"keyword", "timestamp", "results"}]}
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = {}

    def _save(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)

    def add(self, user: str, keyword: str, num_results: int):
        if user not in self.history:
            self.history[user] = []
        self.history[user].append({
            "keyword": keyword,
            "timestamp": str(datetime.now()),
            "results": num_results
        })
        self._save()

    def get_user_history(self, user: str, limit: int = 10):
        return self.history.get(user, [])[-limit:]

    def display(self, user: str, limit: int = 10):
        print("\n" + "=" * 70)
        print(f"SEARCH HISTORY — {user}")
        print("=" * 70)
        print(f"{'Timestamp':<28} {'Keyword':<20} {'Results'}")
        print("-" * 70)

        records = self.get_user_history(user, limit)
        if not records:
            print("   (No search history)")
        else:
            for r in records:
                print(f"{r['timestamp'][:26]:<28} {r['keyword']:<20} {r['results']}")
        print("=" * 70)

    def get_top_keywords(self, limit: int = 5):
        counter = {}
        for user, records in self.history.items():
            for r in records:
                kw = r["keyword"].lower()
                counter[kw] = counter.get(kw, 0) + 1
        sorted_kw = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        return sorted_kw[:limit]