# Medicine Assistant App - Backend (Django)

This is the **backend** for the Medicine Assistant App, built with **Django** and **Django REST Framework**.  
It provides CRUD APIs for managing pharmacies, medicines, prescriptions, and reminders.  
Currently, it uses **in-memory or SQLite storage** for testing purposes.

---

##  Features
- Manage **Pharmacies** and their inventory
- Manage **Medicines** with details like name, stock, and expiry
- **Doctors** can add prescriptions for patients
- **Customers** can upload prescriptions (OCR support planned)
- Google Maps API integration (planned) for pharmacy location search
- OCR API integration (planned) for reading prescription images

---

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Frontend (planned):** Flutter
- **Database:** SQLite (default for development)
- **APIs:** Google Maps API, OCR API (future)

---

##  Getting Started

### 1️ Clone the Repository

git clone https://github.com/yourusername/medicine-assistant-backend.git

cd medicine-assistant-backend


Create and Activate Virtual Environment

python -m venv env

env\Scripts\activate

Run migrations

python manage.py makemigrations

python manage.py migrate

Run server

python manage.py runserver

