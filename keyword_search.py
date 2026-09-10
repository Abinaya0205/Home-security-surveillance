# search/keyword_search.py
from crypto.aes_cipher import AESCipher
from config import RANKING_WEIGHTS

class SecureSearch:
    def __init__(self, blockchain, aes_key: bytes):
        self.chain = blockchain
        self.aes = AESCipher()
        self.key = aes_key

    def encrypt_query(self, keyword: str) -> str:
        return self.aes.encrypt_keyword(keyword, self.key)

    def _calculate_score(self, block_data: dict, keyword: str, block_index: int) -> int:
        """Ranking score based on multiple factors"""
        score = 0
        weights = RANKING_WEIGHTS

        # Factor 1: Recency — newer blocks get higher score
        chain_length = len(self.chain.chain)
        recency_score = (block_index / chain_length) * weights["recency"]
        score += recency_score

        # Factor 2: Owner priority — owner's files ranked higher
        if block_data.get("owner") == "owner":
            score += weights["owner_priority"]

        # Factor 3: Keyword position in filename
        file_id = block_data.get("file_id", "").lower()
        if keyword.lower() in file_id:
            score += weights["exact_match"]
        elif any(part in file_id for part in keyword.lower().split("_")):
            score += weights["partial_match"]

        return round(score, 2)

    def search(self, keyword: str, top_k: int = 5):
        """Encrypted query → match → rank → return top K"""
        enc_query = self.encrypt_query(keyword)
        print(f"[SEARCH] Keyword: '{keyword}'")
        print(f"         Encrypted query: {enc_query[:20]}...")

        raw_results = self.chain.search_by_keyword(enc_query)

        # Add ranking score
        ranked = []
        for block in self.chain.chain:
            if block.data in raw_results:
                score = self._calculate_score(block.data, keyword, block.index)
                ranked.append({"data": block.data, "score": score, "block_index": block.index})

        # Sort by score (highest first)
        ranked.sort(key=lambda x: x["score"], reverse=True)

        print(f"[RANKING] Ranked {len(ranked)} result(s):")
        for i, r in enumerate(ranked[:top_k], 1):
            print(f"   #{i} Score={r['score']}  File={r['data']['file_id']}")

        return [r["data"] for r in ranked[:top_k]]