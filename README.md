Django Basic Project
====================

Project Overview
----------------
This is a basic Django project that serves as a starting point for building web applications. 
It includes a simple Django structure with models, views, templates, and static files.

Project Structure
-----------------
/gutenberg
│── books/                   # Django app
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files (CSS, JS, Images)
│   ├── templates/           # HTML templates
│   ├── views.py             # Application views
│   ├── models.py            # Database models
│   ├── urls.py              # URL configuration
│── my_project/              # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Project-level URLs
│   ├── wsgi.py              # WSGI entry point
│── manage.py                # Django CLI tool
│── requirements.txt         # Python dependencies
│── README.txt               # Project documentation

Installation & Setup
--------------------
1. Clone the Repository:
   git clone https://github.com/mskannan/gutenberg.git
   cd your-repo

2. Create a Virtual Environment:
   python -m venv venv
   On macOS/Linux: source venv/bin/activate
   On Windows: venv\Scripts\activate

3. Install Dependencies:
   pip install -r requirements.txt
 
4. Run the Development Server:
   python manage.py runserver
   Now, open http://127.0.0.1:8000/ in your browser.

Features
--------
- Django-based web application
- User authentication system
- Admin panel for managing data
- Database integration (SQLite by default)
- Static files handling (CSS, JavaScript, Images)

Common Commands
---------------
python manage.py startapp app_name   - Create a new Django app
python manage.py makemigrations      - Generate migration files
python manage.py migrate             - Apply migrations to DB
python manage.py runserver           - Start development server
python manage.py shell               - Open Django shell

License
-------
This project is open-source and available under the MIT License.

Contributions
-------------
Feel free to contribute by creating issues, pull requests, or suggesting new features.
