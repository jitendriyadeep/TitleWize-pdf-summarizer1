# PDF Summarizer

A **Django-based web application** that allows users to upload PDF files and generate summaries in different lengths (short, medium, long).

🔗 **Live Demo:** [Add your deployed link here]

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

### 1. Clone the Repository

git clone https://github.com/jitendriyadeep/TitleWize-pdf-summarizer1.git

cd TitleWize-pdf-summarizer

### 2. Set Up a Virtual Environment

python -m venv venv

#### Activate the environment:

##### Windows:

venv\Scripts\activate

##### Linux/Mac:

source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up the Database

python manage.py migrate

### 5. Create a Superuser (Admin)

python manage.py createsuperuser
--->Follow prompts to create admin credentials.<---

### 6. Run the Development Server

python manage.py runserver
➡️ Open http://127.0.0.1:8000 in your browser.

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
