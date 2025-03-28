# PDF Summarizer

A **Django-based web application** that allows users to upload PDF files and generate summaries in different lengths (short, medium, long).

🔗 **Live Demo:** COMING SOON !!!

---

## ✨ Features

### 1️⃣ User Authentication

- **Register** with a username and password
- **Login** securely to access personalized features
- **Logout** to ensure session security
- **Password Reset** via email if forgotten

### 2️⃣ PDF Processing

- **Upload PDF files** directly to the system
- **Generate summaries** in three modes:
  - **Short** (Key points only)
  - **Medium** (Concise overview)
  - **Long** (Detailed summary)

### 3️⃣ User History

- **Track all past summaries** in a dedicated dashboard
- **View, download, or delete** previous summaries

---

## 🛠️ Installation & Setup

### 0. Clone the Repository

git clone https://github.com/jitendriyadeep/TitleWize-pdf-summarizer1.git

cd TitleWize-pdf-summarizer1

### 1. Set Up a Virtual Environment

python -m venv venv

#### Activate the environment:

##### Windows:

venv\Scripts\activate

##### Linux/Mac:

source venv/bin/activate

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Configure the .env file in the root folder

DJANGO_SECRET_KEY= "your_secret_key"

DB_NAME="your_db_name"

DB_USER="your_user_name"

DB_PASSWORD="your_password"

DB_HOST=localhost

DB_PORT=5432

GEMINI_API_KEY="your_api_key"

Although i have given values according to me which can run for a while.
kindly dont misuse it , as those values are under my name.

### 4. Change the directory where the manage.py file is there

cd summarizer

### 5. Create a Database

python manage.py makemigrations

python manage.py migrate

### 6. Create a Superuser (Admin)

python manage.py createsuperuser

--->Follow prompts to create admin credentials.<---

### 7. Run the Development Server

python manage.py runserver
➡️ Open http://127.0.0.1:8000 in your browser.

##### if after running the server a error is coming such as

###### "You're accessing the development server over HTTPS, but it only supports HTTP."

###### then try one of the below 3 steps:

->Explicitly type http://127.0.0.1:8000 (not https) in your address bar

->Clear your browser cache completely (Ctrl+Shift+Del in most browsers) [works mostly]

->Try using an incognito/private window

### 📂 Project Structure

TitleWize-pdf-summarizer/
├── pdf_processor/ # Handles PDF uploads & summaries
├── users/ # User authentication & profiles
├── templates/ # HTML frontend files
├── static/ # CSS, JS, and assets
├── manage.py # Django management script
└── requirements.txt # Python dependencies

### 🔧 Technologies Used

##### Backend: Django, Django REST Framework

##### Frontend: HTML, CSS, Bootstrap

##### Database: SQLite (development), PostgreSQL (production)

##### PDF Processing: Gemini-2.0-flash, PyPDF2, NLTK/Spacy for text summarization

##### Authentication: Django Allauth
