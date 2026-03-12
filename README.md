# 🧠 NeuroFlow: Post-Op Neurosurgery Portal

## Description
NeuroFlow is a medical management web application designed to bridge the gap between clinical surgery and home recovery. It allows patients to log vitals and symptoms while giving doctors a prioritized dashboard for intervention.

## Features
- **Dual-Role Access:** Dedicated interfaces for Medical Staff and Patients.
- **Emergency Detection:** Real-time scanning of patient logs for critical neurological symptoms.
- **Holistic Tracking:** Monitors hydration and local weather patterns to correlate with recovery.
- **Security:** Implements PBKDF2 password hashing and Flask-Limiter for data protection.

## Technologies
- Python 3.9
- Flask Framework
- SQLite3 (Relational Database)
- HTML5 / CSS3 / JavaScript

## Installation & Usage
```bash
# Clone the repository
git clone [https://github.com/YOUR-USERNAME/NeuroFlow-Portal.git](https://github.com/YOUR-USERNAME/NeuroFlow-Portal.git)

# Install requirements
pip install -r requirements.txt

# Run the app
python app.py