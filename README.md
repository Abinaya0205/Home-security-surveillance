# 🔐 Home Security Surveillance System

> A Blockchain-Based Secure IoT Data Sharing Framework with Hybrid ECC-AES Encryption and Encrypted Keyword Search

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Blockchain](https://img.shields.io/badge/Blockchain-Custom-orange)
![Encryption](https://img.shields.io/badge/Encryption-ECC%20%2B%20AES-green)

---

## 📌 Overview

A blockchain-enabled secure data sharing system designed for **home security surveillance** environments. The system combines **hybrid cryptography (ECC + AES)** with an **immutable blockchain audit trail** to ensure data confidentiality, integrity, and privacy-preserving search over encrypted IoT data stored in the cloud.

Suitable for:
- 🏠 Home Security Surveillance
- 🏭 Industrial IoT Deployments
- 🏙️ Smart City Data Management

---

## ✨ Key Features

 Feature | Description 

🔐 **Hybrid ECC + AES Encryption** | ECDH key exchange (SECP256R1) + AES-256-CBC for end-to-end data protection 
⛓️ **Blockchain Audit Trail** | Immutable SHA-256 hash-linked chain for all data access events 
🔍 **Encrypted Keyword Search** | Privacy-preserving search — keywords encrypted before cloud query 
👥 **Multi-User RBAC** | Role-based access control: admin / premium / basic / guest 
📊 **Ranking Algorithm** | Score-based relevance sorting (recency, owner priority, match type) 
🚨 **Security Alerts** | Real-time WARNING / CRITICAL alerts for unauthorized access 
📁 **File Preview + Metadata** | Preview file info (size, owner, block hash, timestamp) before download 
📈 **Admin Dashboard** | Statistics: total blocks, users, searches, top keywords, alerts 
🔎 **Search History** | Per-user search tracking with top keyword analytics 
📝 **Activity Logs** | Complete audit trail of user actions (login, search, download) 
🛡️ **Tamper Detection** | Instant chain invalidation on any modification 
☁️ **Cloud Storage** | Local simulation + AWS S3 integration ready 

---
## 🏗️ System Architecture

┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ IoT Data │─────▶│ ECC + AES │─────▶│ Cloud │
│ Sources │ │ Hybrid │ │ Storage │
│ (Home Sensors) │ │ Encryption │ │ (S3 / Local) │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│
▼
┌─────────────────┐
│ Blockchain │◀──── Immutable Audit
│ (SHA-256) │
└─────────────────┘
│
▼
┌─────────────────┐
│ Multi-User │
│ RBAC + │
│ Encrypted │
│ Search │
└─────────────────┘


---

## 🛠️ Tech Stack

Category | Technology |

**Language** | Python 3.11 
**Cryptography** | `cryptography` (ECC SECP256R1, AES-256-CBC, HKDF, SHA-256) 
**Blockchain** | Custom implementation (SHA-256 hash-linked) 
**Storage** | Local simulation + `boto3` (AWS S3 ready) 
**Data Processing** | `pandas` 
**Security** | RBAC, Encrypted Keyword Search, Audit Logging 

---


### Steps

# 1. Clone the repository
git clone https://github.com/Abinaya0205/Home-security-surveillance.git
cd Home-security-surveillance

# Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate


# Install dependencies
pip install -r requirements.txt


## Usage
python main.py

## Menu-Driven Interface
--- MENU ---
  1. Secure Search (with file preview)
  2. My Search History
  3. My Activity Logs
  4. Admin Statistics Dashboard
  5. View Security Alerts
  6. Logout
  7. Exit

## Demo Login Credentials

	Role	Access Level
owner	Admin	Full access + Dashboard + Alerts
user1	Premium	All keyword search
user2	Basic	Restricted: camera, door_lock, front_door
user3	Guest	Restricted: camera only


📊 Project Structure

## Home-security-surveillance/
├── main.py                      # Entry point (menu-driven CLI)
├── config.py                    # Configuration (users, alerts, ranking)
├── requirements.txt
├── .gitignore
│
├── blockchain/                  # Custom blockchain
│   ├── __init__.py
│   ├── block.py
│   └── chain.py
│
├── crypto/                      # Hybrid cryptography
│   ├── __init__.py
│   ├── ecc_cipher.py            # ECC (SECP256R1, ECDH)
│   ├── aes_cipher.py            # AES-256-CBC
│   └── hybrid.py                # Combined ECC + AES
│
├── search/                      # Encrypted search + ranking
│   ├── __init__.py
│   └── keyword_search.py
│
├── users/                       # Multi-user management
│   ├── __init__.py
│   └── user_manager.py
│
├── audit/                       # Audit & alerts
│   ├── __init__.py
│   ├── access_log.py
│   ├── search_history.py
│   └── alerts.py
│
├── dashboard/                   # Admin statistics
│   ├── __init__.py
│   └── stats.py
│
├── preview/                     # File metadata preview
│   ├── __init__.py
│   └── file_preview.py
│
└── cloud/                       # Cloud storage
    ├── __init__.py
    ├── local_storage.py         # Local simulation
    └── aws_s3.py                # AWS S3 (optional)
🔒 Security Highlights
✅ End-to-End Encryption — Data encrypted before cloud upload

✅ Zero Plaintext Keywords — Search queries encrypted before matching

✅ Immutable Audit Trail — Every access logged on blockchain

✅ Tamper-Proof — Any modification breaks chain validity

✅ Least Privilege — Role-based permission enforcement

✅ Real-Time Alerts — Instant notification on unauthorized attempts

✅ Privacy-Preserving Search — Cloud server never sees plaintext queries

🧪 Sample Workflow
Owner uploads encrypted IoT dataset to cloud

Blockchain records file metadata (hash, keywords, owner)

User logs in with role-based credentials

User searches with encrypted keyword

Ranking algorithm scores results by relevance

File preview shows metadata before download

Authorized user decrypts file with shared AES key

Blockchain logs every action for audit

📈 Performance Metrics
The system demonstrates improved performance over centralized cloud systems in terms of:

Recall — Higher retrieval of relevant files

Precision — Accurate match results

Ranking — Relevance-based ordering

Privacy — Query confidentiality preserved

Search Time — Optimized encrypted matching

🚧 Future Enhancements

□ Zero-knowledge proof integration
□ IPFS decentralized storage
□ Smart contract-based access control (Ethereum)
□ Multi-blockchain consensus
□ Web dashboard (React + FastAPI)
□ Mobile app integration
□ Real-time video surveillance integration


👤 Author
Abinaya.T

GitHub: @Abinaya0205

🙏 Acknowledgments

Built with Python cryptography library

Inspired by blockchain + IoT security research

Special thanks to project guide and mentors



## 🏗️ System Architecture
