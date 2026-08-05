"""
Pavithira J — Full Stack Developer Portfolio
Flask backend

Serves the single-page portfolio, exposes a small REST API for the
projects / skills / certifications data, and stores contact-form
submissions in MySQL after validating them.
"""

import os
import re
import logging
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb

# --------------------------------------------------------------------------
# App configuration
# --------------------------------------------------------------------------

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "portfolio_db")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("portfolio")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# --------------------------------------------------------------------------
# Static content (kept in Python for now; easy to move to MySQL/JSON later)
# --------------------------------------------------------------------------

PROFILE = {
    "name": "Pavithira J",
    "title": "Full Stack Developer",
    "summary": (
        "I am a passionate Full Stack Developer with a strong interest in "
        "building modern, responsive, and user-friendly web applications "
        "using Python, Flask, HTML, CSS, JavaScript, and MySQL. I enjoy "
        "learning new technologies and continuously improving my "
        "development skills."
    ),
}

SKILLS = {
    "Frontend": ["HTML5", "CSS3", "JavaScript"],
    "Backend": ["Python", "Flask"],
    "Database": ["MySQL"],
    "Tools": ["Git", "GitHub", "VS Code"],
}

PROJECTS = [
    {
        "id": 1,
        "title": "Inventory Management System",
        "description": (
            "A web app to track stock levels, incoming and outgoing goods, "
            "and low-stock alerts for small businesses."
        ),
        "tech": ["Python", "Flask", "MySQL", "JavaScript"],
    },
    {
        "id": 2,
        "title": "Student Management System",
        "description": (
            "Manages student records, marks, and attendance with a clean "
            "interface for searching and reporting."
        ),
        "tech": ["Python", "Flask", "MySQL", "HTML/CSS"],
    },
    {
        "id": 3,
        "title": "Library Management System",
        "description": (
            "Tracks books, issue/return dates, and availability, built to "
            "make everyday librarian tasks fast and simple."
        ),
        "tech": ["Python", "Flask", "MySQL"],
    },
    {
        "id": 4,
        "title": "Calculator Website",
        "description": (
            "A responsive calculator with a polished UI, keyboard support, "
            "and clean JavaScript logic under the hood."
        ),
        "tech": ["HTML", "CSS", "JavaScript"],
    },
    {
        "id": 5,
        "title": "Advanced Healthcare Chatbot",
        "description": (
            "A conversational assistant that helps users understand "
            "symptoms and points them toward the right kind of care."
        ),
        "tech": ["Python", "Flask", "NLP"],
    },
]

CERTIFICATIONS = [
    {"issuer": "Coursera", "name": "Python for Everybody Specialization"},
    {"issuer": "Naan Mudhalvan", "name": "Oracle Cloud Architecture"},
    {"issuer": "Naan Mudhalvan", "name": "Generative AI"},
    {"issuer": "Naan Mudhalvan", "name": "English Language Communication Assessment"},
    {"issuer": "Illustro", "name": "Introduction to Python Programming"},
    {"issuer": "Illustro", "name": "Data Structures and Algorithms"},
    {"issuer": "Illustro", "name": "Blockchain Application Development"},
    {"issuer": "Illustro", "name": "DevOps"},
]

EDUCATION = [
    {
        "degree": "B.Sc Computer Science",
        "institution": "Shrimathi Indira Gandhi College, Tiruchirappalli",
        "period": "2022 - 2025",
        "details": "Graduated with 75%."
    },
    {
        "degree": "M.Sc Computer Science",
        "institution": "Shrimathi Indira Gandhi College, Tiruchirappalli",
        "period": "2025 - Present",
        "details": "Currently pursuing M.Sc in Computer Science(2nd year)"
    },
]
SOCIALS = {
    "email": "pavithirajeganathan@gmail.com",
    "github": "https://github.com/Pavithirajeganthan",
    "linkedin": "https://www.linkedin.com/in/pavithira-jeganathan",
    "resume": "/static/files/Pavithira_Resume.pdf"
}

# --------------------------------------------------------------------------
# Page routes
# --------------------------------------------------------------------------


@app.route("/")
def index():
    return render_template(
    "index.html",
    profile=PROFILE,
    skills=SKILLS,
    projects=PROJECTS,
    certifications=CERTIFICATIONS,
    education=EDUCATION,
    socials=SOCIALS,
)


# --------------------------------------------------------------------------
# REST API
# --------------------------------------------------------------------------


@app.route("/api/profile", methods=["GET"])
def api_profile():
    return jsonify(PROFILE)


@app.route("/api/skills", methods=["GET"])
def api_skills():
    return jsonify(SKILLS)


@app.route("/api/projects", methods=["GET"])
def api_projects():
    return jsonify(PROJECTS)


@app.route("/api/certifications", methods=["GET"])
def api_certifications():
    return jsonify(CERTIFICATIONS)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "message": "Portfolio API is working"
    })


@app.route("/api/contact", methods=["POST"])
def api_contact():
    """Validate and store a contact-form submission in MySQL."""
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}
    if not name or len(name) < 2:
        errors["name"] = "Please enter your full name."
    if not email or not EMAIL_RE.match(email):
        errors["email"] = "Please enter a valid email address."
    if not subject or len(subject) < 3:
        errors["subject"] = "Please enter a subject."
    if not message or len(message) < 10:
        errors["message"] = "Message should be at least 10 characters."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO messages (name, email, subject, message, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, email, subject, message, datetime.utcnow()),
        )
        mysql.connection.commit()
        cursor.close()
    except MySQLdb.MySQLError as exc:
        logger.error("Database error while saving contact message: %s", exc)
        return jsonify({
            "success": False,
            "errors": {"server": "Could not save your message right now. Please try again shortly."},
        }), 500

    return jsonify({"success": True, "message": "Thanks for reaching out! I'll get back to you soon."}), 201


# --------------------------------------------------------------------------
# Error handlers
# --------------------------------------------------------------------------


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(_error):
    logger.error("Internal server error: %s", _error)
    return render_template("500.html"), 500


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug_mode)
