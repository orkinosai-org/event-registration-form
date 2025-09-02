"""
Configuration settings for the Event Registration Form application.
"""
import os
from typing import List

# Email configuration (for demonstration purposes)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your-email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-app-password")
FROM_EMAIL = os.getenv("FROM_EMAIL", "your-email@gmail.com")

# Application settings
APP_NAME = "Event Registration Form"
APP_DESCRIPTION = "A FastAPI application for event registration with email verification"

# Available events for registration
AVAILABLE_EVENTS: List[dict] = [
    {
        "id": "web-dev-2024",
        "name": "Web Development Bootcamp 2024",
        "description": "Learn modern web development with React, Node.js, and databases",
        "date": "2024-03-15",
        "duration": "8 weeks"
    },
    {
        "id": "python-ml-2024", 
        "name": "Python for Machine Learning",
        "description": "Master machine learning with Python, pandas, and scikit-learn",
        "date": "2024-04-01",
        "duration": "6 weeks"
    },
    {
        "id": "cloud-aws-2024",
        "name": "AWS Cloud Fundamentals",
        "description": "Learn AWS services, deployment, and cloud architecture",
        "date": "2024-04-20",
        "duration": "4 weeks"
    },
    {
        "id": "mobile-dev-2024",
        "name": "Mobile App Development",
        "description": "Build mobile apps with React Native and Flutter",
        "date": "2024-05-10", 
        "duration": "10 weeks"
    }
]

# Verification code settings
VERIFICATION_CODE_LENGTH = 6
VERIFICATION_CODE_EXPIRY_MINUTES = 15