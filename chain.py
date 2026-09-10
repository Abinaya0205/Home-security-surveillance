from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, {"info": "Genesis"}, "0")]

    def add_block(self, data):
        prev = self.chain[-1]
        new_block = Block(len(self.chain), data, prev.hash)
        self.chain.append(new_block)
        return new_block

    def search_by_keyword(self, encrypted_keyword):
        results = []
        for block in self.chain:
            if "keywords_enc" in block.data:
                if encrypted_keyword in block.data["keywords_enc"]:
                    results.append(block.data)
        return results

    def is_valid(self):
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i-1]
            if cur.hash != cur.calculate_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
        return True