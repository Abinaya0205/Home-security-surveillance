# audit/access_log.py
import os
from datetime import datetime

class AccessLog:
    """Logs all user activities — searches, logins, uploads, denials"""

    def __init__(self, blockchain, log_file="audit/access_log.txt"):
        self.blockchain = blockchain
        self.log_file = log_file
        self.entries = []           # In-memory log list
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log(self, user: str, action: str, details: dict = None, status: str = "SUCCESS"):
        entry = {
            "timestamp": str(datetime.now()),
            "user": user,
            "action": action,             # LOGIN, SEARCH, UPLOAD, DOWNLOAD, DENIED
            "details": details or {},
            "status": status              # SUCCESS, DENIED, FAILED
        }
        self.entries.append(entry)

        # Append to file
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{entry['timestamp']}] {user} | {action} | {status} | {entry['details']}\n")

        # Blockchain-la log pannunga (immutable)
        self.blockchain.add_block({
            "type": "ACCESS_LOG",
            "user": user,
            "action": action,
            "status": status,
            "timestamp": entry["timestamp"],
            "details": entry["details"]
        })

    def get_user_logs(self, user: str = None, limit: int = 10):
        if user:
            filtered = [e for e in self.entries if e["user"] == user]
        else:
            filtered = self.entries
        return filtered[-limit:]

    def get_denied_logs(self, limit: int = 10):
        return [e for e in self.entries if e["status"] == "DENIED"][-limit:]

    def display(self, user: str = None, limit: int = 15):
        print("\n" + "=" * 90)
        print(f"{'ACCESS LOG':^90}")
        print("=" * 90)
        print(f"{'Timestamp':<28} {'User':<10} {'Action':<12} {'Status':<10} {'Details'}")
        print("-" * 90)

        logs = self.get_user_logs(user, limit)
        if not logs:
            print("   (No logs found)")
        else:
            for e in logs:
                details_str = str(e["details"])[:30]
                print(f"{e['timestamp'][:26]:<28} {e['user']:<10} {e['action']:<12} {e['status']:<10} {details_str}")
        print("=" * 90)