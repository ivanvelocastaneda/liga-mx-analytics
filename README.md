# ⚽ Liga MX Analytics Dashboard

This project is a web-based analytics dashboard for Liga MX, built with Django and MySQL. It displays various statistical views such as average attendance, player stats, team performance, and more using optimized database views.

## 🚀 Features

- Dynamic dashboard with Bootstrap styling
- Clean team/player statistics with human-readable labels
- MySQL views for fast, optimized analytics queries
- Environment-agnostic setup via virtualenv and `requirements.txt`

## 🏗️ Tech Stack

- Python 3.11
- Django 5.x
- MySQL
- Bootstrap 5
- HTML/CSS
- PyMySQL / mysqlclient
- sqlparse

## 📁 Project Structure
liga_mx_analytics/ 
├── env/ # virtualenv (excluded from Git) 
├── liga_mx_analytics/ # Django project settings 
│ └── stats/ # Main app: views, templates, models 
│ └── base.html
│ └── dashboard.html 
│ └── static/ styles.css
├── manage.py 
├── .gitignore 
├── requirements.txt 
└── README.md

## ⚙️ Setup Instructions
1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/liga-mx-analytics.git
   cd liga-mx-analytics

2. **Create a virtual environment**
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt   

4. **Configure your database**
Update settings.py with your MySQL DB name, user, and password.