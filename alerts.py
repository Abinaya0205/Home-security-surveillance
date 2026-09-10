# audit/alerts.py
import os
from datetime import datetime
from config import ALERTS

class AlertSystem:
    """Detects and logs unauthorized access + security alerts"""

    def __init__(self):
        self.alerts = []
        self.failed_attempts = {}        # {user: count}
        self.alert_log = ALERTS["log_file"]
        os.makedirs(os.path.dirname(self.alert_log), exist_ok=True)

    def _write_alert(self, level: str, user: str, message: str):
        alert = {
            "timestamp": str(datetime.now()),
            "level": level,           # INFO, WARNING, CRITICAL
            "user": user,
            "message": message
        }
        self.alerts.append(alert)

        with open(self.alert_log, "a", encoding="utf-8") as f:
            f.write(f"[{alert['timestamp']}] [{level}] {user} | {message}\n")

        # Print to console with color-like indicator
        symbol = {"INFO": "[i]", "WARNING": "[!]", "CRITICAL": "[X]"}.get(level, "[*]")
        print(f"\n{symbol} SECURITY ALERT [{level}]")
        print(f"   User: {user}")
        print(f"   Message: {message}\n")

    def unauthorized_access(self, user: str, attempted_action: str, reason: str = ""):
        if ALERTS["unauthorized_access"]:
            self._write_alert(
                "CRITICAL", user,
                f"Unauthorized {attempted_action} attempt. {reason}"
            )

    def restricted_keyword(self, user: str, keyword: str):
        if ALERTS["restricted_keyword"]:
            self._write_alert(
                "WARNING", user,
                f"Restricted keyword searched: '{keyword}'"
            )

    def failed_attempt(self, user: str, reason: str = ""):
        self.failed_attempts[user] = self.failed_attempts.get(user, 0) + 1
        count = self.failed_attempts[user]

        if count >= ALERTS["multiple_failed_attempts"]:
            self._write_alert(
                "CRITICAL", user,
                f"Multiple failed attempts ({count}). Reason: {reason}"
            )
        else:
            self._write_alert(
                "WARNING", user,
                f"Failed attempt #{count}. Reason: {reason}"
            )

    def display_recent(self, limit: int = 10):
        print("\n" + "=" * 80)
        print("RECENT SECURITY ALERTS")
        print("=" * 80)
        if not self.alerts:
            print("   (No alerts — system secure)")
        else:
            for a in self.alerts[-limit:]:
                print(f"[{a['level']:<8}] {a['timestamp'][:19]} | {a['user']:<10} | {a['message']}")
        print("=" * 80)