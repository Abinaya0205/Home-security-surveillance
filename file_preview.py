# preview/file_preview.py
import os
from datetime import datetime

class FilePreview:
    """Displays file metadata + preview before download"""

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def get_metadata(self, file_id: str) -> dict:
        """Find file metadata from blockchain"""
        for block in self.blockchain.chain:
            if block.data.get("file_id") == file_id:
                return {
                    "file_id": file_id,
                    "block_index": block.index,
                    "block_hash": block.hash[:32] + "...",
                    "timestamp": block.timestamp,
                    "owner": block.data.get("owner", "unknown"),
                    "cloud_path": block.data.get("cloud_path"),
                    "keywords_indexed": len(block.data.get("keywords_enc", []))
                }
        return None

    def display(self, file_id: str, encrypted_path: str = None):
        """Show file preview card"""
        meta = self.get_metadata(file_id)
        if not meta:
            print(f"[PREVIEW] No metadata for {file_id}")
            return

        # File size (encrypted)
        size = "unknown"
        if encrypted_path and os.path.exists(encrypted_path):
            size_bytes = os.path.getsize(encrypted_path)
            size = f"{size_bytes} bytes"

        print("\n" + "┌" + "─" * 60 + "┐")
        print(f"│ {'📄 FILE PREVIEW':<58} │")
        print("├" + "─" * 60 + "┤")
        print(f"│ File ID       : {meta['file_id']:<40} │")
        print(f"│ Owner         : {meta['owner']:<40} │")
        print(f"│ Block Index   : {meta['block_index']:<40} │")
        print(f"│ Block Hash    : {meta['block_hash']:<40} │")
        print(f"│ Timestamp     : {meta['timestamp'][:19]:<40} │")
        print(f"│ Encrypted Size: {size:<40} │")
        print(f"│ Keywords      : {meta['keywords_indexed']} encrypted keyword(s){'':<19} │")
        print(f"│ Storage Path  : {str(meta['cloud_path'])[:40]:<40} │")
        print("└" + "─" * 60 + "┘")