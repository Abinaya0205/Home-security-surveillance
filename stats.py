# dashboard/stats.py
from datetime import datetime

class StatisticsDashboard:
    """Admin dashboard — total stats + analytics"""

    def __init__(self, blockchain, access_log, search_history, alert_system, user_mgr):
        self.blockchain = blockchain
        self.access_log = access_log
        self.search_history = search_history
        self.alerts = alert_system
        self.user_mgr = user_mgr

    def display(self):
        chain = self.blockchain.chain
        total_blocks = len(chain)
        files = [b for b in chain if "file_id" in b.data]
        access_logs = [b for b in chain if b.data.get("type") == "ACCESS_LOG"]
        denied = [e for e in self.access_log.entries if e["status"] == "DENIED"]
        searches = sum(len(v) for v in self.search_history.history.values())

        print("\n" + "=" * 70)
        print(f"{'ADMIN STATISTICS DASHBOARD':^70}")
        print("=" * 70)

        print(f"\n📊 BLOCKCHAIN")
        print(f"   Total Blocks       : {total_blocks}")
        print(f"   Files Stored       : {len(files)}")
        print(f"   Access Log Blocks  : {len(access_logs)}")
        print(f"   Chain Valid        : {'✅ Yes' if self.blockchain.is_valid() else '❌ No'}")

        print(f"\n👥 USERS")
        for user in self.user_mgr.user_info.keys():
            role = self.user_mgr.get_role(user)
            print(f"   {user:<10} : {role}")

        print(f"\n🔍 SEARCH ACTIVITY")
        print(f"   Total Searches     : {searches}")
        top_kw = self.search_history.get_top_keywords(5)
        if top_kw:
            print(f"   Top Keywords:")
            for kw, count in top_kw:
                print(f"      - {kw:<20} : {count} time(s)")

        print(f"\n🚨 SECURITY")
        print(f"   Total Alerts       : {len(self.alerts.alerts)}")
        print(f"   Denied Accesses    : {len(denied)}")
        critical = [a for a in self.alerts.alerts if a["level"] == "CRITICAL"]
        print(f"   Critical Alerts    : {len(critical)}")

        print(f"\n📁 STORAGE")
        print(f"   Storage Mode       : LOCAL/AWS")
        print(f"   Users Configured   : {len(self.user_mgr.user_info)}")

        print("\n" + "=" * 70)
        print(f"   Report generated at: {datetime.now()}")
        print("=" * 70)