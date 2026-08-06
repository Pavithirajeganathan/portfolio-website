# Portfolio Website

## Live Demo
https://portfolio-website-p5o1.onrender.com

## Technologies Used
- Python
- Flask
- HTML
- CSS
- JavaScript
- # Pavithira J — Full Stack Developer Portfolio

A premium, responsive portfolio site with a Flask + MySQL backend.
Dark theme, blue/purple gradients, glassmorphism cards, typing effect,
and a contact form that saves messages to a database.

## Tech stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL

## Project structure

```
portfolio/
├── app.py                 # Flask app, routes, REST API, contact form handling
├── requirements.txt        # Python dependencies
├── database.sql             # MySQL schema
├── templates/
│   ├── index.html          # Main single-page site
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── css/style.css       # Theme, layout, animations
│   ├── js/script.js        # Typing effect, nav, scroll reveal, form submit
│   └── images/             # Add your photos/screenshots here
└── README.md
```

## 1. Prerequisites

- Python 3.10+
- MySQL Server 8.0+ (or MariaDB)
- `pip`

### System packages for `mysqlclient`

`mysqlclient` compiles against MySQL's client library, so install the dev
headers first:

**Ubuntu / Debian**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

**macOS (Homebrew)**
```bash
brew install mysql-client pkg-config
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

**Windows**
Use the prebuilt wheel — `pip install mysqlclient` normally works out of
the box with recent Python versions.

## 2. Set up the database

```bash
mysql -u root -p < database.sql
```

This creates the `portfolio_db` database and a `messages` table for
contact-form submissions.

## 3. Configure environment variables

Create a `.env` file in the project root (or export these in your shell):

```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=portfolio_db
FLASK_DEBUG=true
```

## 4. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 5. Run locally

```bash
python app.py
```

Visit **http://127.0.0.1:5000**

## 6. Deploying to production

- Set `FLASK_DEBUG=false`
- Run behind a WSGI server: `gunicorn -w 4 app:app`
- Put it behind Nginx or a platform like Render / Railway / PythonAnywhere
- Use a managed MySQL instance (PlanetScale, AWS RDS, etc.) and update the
  `MYSQL_*` environment variables accordingly

## Customizing content

All text content (profile, skills, projects, certifications, education)
lives in the top of `app.py` as plain Python dictionaries/lists — edit
those directly, no template digging required. Update the placeholder
email/GitHub/LinkedIn links in `templates/index.html` under the Contact
section, and drop real project links in the `PROJECTS` list in `app.py`
if you have live demos or repos to point to.

## What's intentionally not included

Per the project brief, this portfolio has **no login page, admin
dashboard, authentication, or user management** — it's a public-facing
site with a simple, validated contact form as its only write operation.
