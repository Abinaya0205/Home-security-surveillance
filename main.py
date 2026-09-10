# main.py
import os
import pandas as pd
from crypto.hybrid import HybridCrypto
from crypto.aes_cipher import AESCipher
from blockchain.chain import Blockchain
from search.keyword_search import SecureSearch
from users.user_manager import UserManager
from audit.access_log import AccessLog
from audit.search_history import SearchHistory
from audit.alerts import AlertSystem
from dashboard.stats import StatisticsDashboard
from preview.file_preview import FilePreview
from config import STORAGE_MODE, USERS

# ---------- Setup ----------
os.makedirs("data", exist_ok=True)
dataset = pd.DataFrame({
    "device": ["camera", "motion_sensor", "door_lock", "thermostat", "camera", "door_lock"],
    "event": ["motion_detected", "intrusion_alert", "door_opened", "temp_high", "person_detected", "door_opened"],
    "location": ["front_door", "backyard", "main_gate", "living_room", "living_room", "back_gate"]
})
dataset.to_csv("data/iot_dataset.csv", index=False)
print(f"[OK] IoT dataset created with {len(dataset)} records\n")

print("=" * 60)
print("MULTI-USER SETUP")
print("=" * 60)
user_mgr = UserManager()
user_keys = user_mgr.setup_all_users()
print()

# Storage
if STORAGE_MODE == "aws":
    from cloud.aws_s3 import AWSS3Storage
    storage = AWSS3Storage()
else:
    from cloud.local_storage import LocalStorage
    storage = LocalStorage()

# Core components
blockchain = Blockchain()
aes = AESCipher()
hybrid = HybridCrypto()
owner_key = user_keys["owner"]

# Audit + Dashboard + Preview
access_log = AccessLog(blockchain)
search_history = SearchHistory()
alert_system = AlertSystem()
preview = FilePreview(blockchain)

# Upload files
for idx, row in dataset.iterrows():
    filename = f"data/{row['device']}_{idx}.txt"
    content = f"Device: {row['device']}\nEvent: {row['event']}\nLocation: {row['location']}"
    with open(filename, "w") as f:
        f.write(content)

    enc_path = hybrid.encrypt_file(filename, owner_key)
    keywords = [row["device"], row["event"], row["location"]]
    enc_keywords = [aes.encrypt_keyword(k, owner_key) for k in keywords]

    remote_name = os.path.basename(enc_path)
    storage.upload(enc_path, remote_name)

    blockchain.add_block({
        "file_id": remote_name,
        "keywords_enc": enc_keywords,
        "owner": "owner",
        "cloud_path": remote_name
    })
    print(f"[UPLOAD] {remote_name}")

print(f"\n[CHAIN] Blocks: {len(blockchain.chain)} | Valid: {blockchain.is_valid()}\n")

dashboard = StatisticsDashboard(blockchain, access_log, search_history, alert_system, user_mgr)


# ---------- Helper functions ----------
def do_search(user: str):
    if not user_mgr.can_search(user):
        access_log.log(user, "SEARCH", status="DENIED", details={"reason": "no search permission"})
        alert_system.unauthorized_access(user, "SEARCH", "No permission")
        return

    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        return

    if not user_mgr.is_keyword_allowed(user, keyword):
        access_log.log(user, "SEARCH", status="DENIED", details={"keyword": keyword, "reason": "restricted keyword"})
        alert_system.restricted_keyword(user, keyword)
        print(f"[DENIED] User '{user}' not allowed to search '{keyword}'.")
        return

    access_log.log(user, "SEARCH", details={"keyword": keyword})
    engine = SecureSearch(blockchain, user_keys[user])
    results = engine.search(keyword)
    search_history.add(user, keyword, len(results))
    print(f"[HISTORY] Saved: '{keyword}' for user '{user}'")

    if not results:
        print("[NO MATCH]")
        return

    top = results[0]
    enc_path = os.path.join("cloud", top["cloud_path"])
    preview.display(top["file_id"], encrypted_path=enc_path)

    out_file = "retrieved_" + top["file_id"].replace(".enc", "")
    storage.download(top["cloud_path"], "cloud/temp_download.enc")
    hybrid.decrypt_file("cloud/temp_download.enc", user_keys[user], out_file)
    print(f"\n[DECRYPT] Saved: {out_file}")
    with open(out_file) as f:
        print("\nFile contents:\n" + f.read())

    access_log.log(user, "DOWNLOAD", details={"file_id": top["file_id"]})

def do_dashboard(user: str):
    if user_mgr.get_role(user) != "admin":
        access_log.log(user, "DASHBOARD", status="DENIED")
        alert_system.unauthorized_access(user, "DASHBOARD", "Not admin")
        print("[DENIED] Only admin can view dashboard.")
        return
    dashboard.display()
    access_log.log(user, "DASHBOARD", status="SUCCESS")


def do_my_history(user: str):
    search_history.display(user)
    access_log.log(user, "VIEW_HISTORY", status="SUCCESS")


def do_my_logs(user: str):
    access_log.display(user)


def do_alerts(user: str):
    if user_mgr.get_role(user) != "admin":
        access_log.log(user, "ALERTS", status="DENIED")
        alert_system.unauthorized_access(user, "ALERTS", "Not admin")
        print("[DENIED] Only admin can view alerts.")
        return
    alert_system.display_recent(15)


def do_logout(user: str):
    access_log.log(user, "LOGOUT", status="SUCCESS")


# ---------- Menu Loop ----------
def menu(user: str):
    print(f"\n{'=' * 60}")
    print(f"  LOGGED IN AS: {user}  (role: {user_mgr.get_role(user)})")
    print(f"{'=' * 60}")

    while True:
        print("\n--- MENU ---")
        print("  1. Secure Search (with file preview)")
        print("  2. My Search History")
        print("  3. My Activity Logs")
        print("  4. Admin Statistics Dashboard")
        print("  5. View Security Alerts")
        print("  6. Logout")
        print("  7. Exit")

        choice = input("\nEnter choice (1-7): ").strip()

        if choice == "1":
            do_search(user)
        elif choice == "2":
            do_my_history(user)
        elif choice == "3":
            do_my_logs(user)
        elif choice == "4":
            do_dashboard(user)
        elif choice == "5":
            do_alerts(user)
        elif choice == "6":
            do_logout(user)
            print(f"[OK] {user} logged out.")
            return "logout"
        elif choice == "7":
            print("[OK] Exiting.")
            return "exit"
        else:
            print("[!] Invalid choice. Try again.")


# ---------- Login Loop ----------
while True:
    print("\n" + "=" * 60)
    print("LOGIN")
    print("=" * 60)
    active_user = input(f"Login as {list(USERS.keys())} (or 'exit'): ").strip()

    if active_user.lower() == "exit":
        print("[OK] Bye!")
        break

    if active_user not in USERS:
        print(f"[ERROR] Unknown user '{active_user}'")
        alert_system.failed_attempt(active_user, "unknown user")
        continue

    access_log.log(active_user, "LOGIN", status="SUCCESS")
    result = menu(active_user)

    if result == "exit":
        break