# 🎓 Event Registration Form

A modern web application built with FastAPI for managing event registrations with email verification. This project serves as a comprehensive learning example for Udemy students studying FastAPI and modern web development.

## 📋 Overview

This application demonstrates how to build a complete web application using FastAPI, featuring:
- Event registration form with multiple event options
- Email verification system with 6-digit codes
- Modern, responsive user interface
- Form validation and error handling
- RESTful API design principles

## 🚀 Features

- **Event Registration**: Users can register for various educational events
- **Email Verification**: Secure registration process with email verification codes
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Real-time Validation**: Client-side and server-side form validation
- **Modern UI**: Clean, professional interface with smooth animations
- **Error Handling**: Comprehensive error handling and user feedback

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic**: Data validation using Python type hints
- **Jinja2**: Templating engine for HTML rendering

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox and animations
- **JavaScript**: Interactive form handling and UX enhancements

### Email Service
- **SMTP**: Email sending capability (simulated for development)
- **Email Templates**: HTML and plain text email formats

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/orkinosai-org/event-registration-form.git
cd event-registration-form
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
# Start the development server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Access the Application
Open your web browser and navigate to:
- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📖 How to Use

### For Students (Registration Process)

1. **Visit the Registration Page**
   - Navigate to http://localhost:8000
   - Fill in your full name and email address
   - Select one of the available events

2. **Email Verification**
   - After submitting the form, check your email (or terminal output in development)
   - Enter the 6-digit verification code
   - Complete your registration

3. **Registration Complete**
   - View your registration confirmation
   - See event details and next steps

### For Developers (Code Structure)

```
event-registration-form/
├── main.py                 # FastAPI application entry point
├── models.py              # Pydantic data models
├── email_service.py       # Email sending functionality
├── config.py              # Application configuration
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── registration_form.html
│   ├── verification_form.html
│   ├── success.html
│   └── error.html
├── static/               # CSS and static files
│   └── style.css
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for production configuration:

```env
# Email Configuration (for production)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Application Settings
VERIFICATION_CODE_EXPIRY_MINUTES=15
```

### Available Events

The application comes with 4 pre-configured example events:
- Web Development Bootcamp 2024
- Python for Machine Learning
- AWS Cloud Fundamentals
- Mobile App Development

You can modify these in `config.py` to add your own events.

## 🎯 Learning Objectives

This project teaches students:

### FastAPI Concepts
- Application structure and organization
- Request handling with forms
- Template rendering with Jinja2
- Data validation with Pydantic
- Error handling and HTTP responses
- Static file serving

### Web Development Best Practices
- Responsive design principles
- Form validation (client and server-side)
- User experience (UX) design
- Progressive enhancement
- Accessibility considerations

### Python Programming
- Object-oriented programming with classes
- Async/await programming
- Type hints and data validation
- File organization and imports
- Configuration management

## 🧪 Testing the Application

### Manual Testing Workflow

1. **Test Registration Form**
   ```bash
   # Start the application
   python main.py
   
   # Open browser to http://localhost:8000
   # Fill out the form with valid data
   # Submit and verify redirect to verification page
   ```

2. **Test Email Verification**
   ```bash
   # Check terminal output for verification code
   # Enter the code on verification page
   # Verify redirect to success page
   ```

3. **Test Error Handling**
   ```bash
   # Try invalid email formats
   # Try empty form fields
   # Try expired verification codes
   ```

### API Testing

Access the automatic API documentation at http://localhost:8000/docs to:
- View all available endpoints
- Test API responses
- Understand request/response schemas

## 🚀 Deployment

### Production Considerations

Before deploying to production:

1. **Configure Real Email Service**
   - Set up SMTP credentials in `email_service.py`
   - Use services like SendGrid, AWS SES, or Gmail

2. **Add Database Storage**
   - Replace in-memory storage with PostgreSQL or MongoDB
   - Implement proper data persistence

3. **Add Security Features**
   - HTTPS configuration
   - Rate limiting
   - CORS configuration
   - Input sanitization

4. **Environment Configuration**
   - Set environment variables
   - Configure logging
   - Set up monitoring

### Deployment Options
- **Heroku**: Easy deployment with Procfile
- **DigitalOcean**: App Platform or Droplets
- **AWS**: Elastic Beanstalk or EC2
- **Docker**: Containerized deployment

## 🎓 Extended Learning

### Next Steps for Students

1. **Add Database Integration**
   - Learn SQLAlchemy with FastAPI
   - Implement user authentication
   - Add event management features

2. **Enhance Email Features**
   - Add email templates
   - Implement password reset
   - Create email preferences

3. **Build REST API**
   - Create JSON API endpoints
   - Add API authentication
   - Implement CRUD operations

4. **Add Advanced Features**
   - Payment integration
   - Calendar integration
   - Notification system
   - Admin dashboard

## 🤝 Contributing

This project is part of a Udemy course. Students are encouraged to:
- Fork the repository
- Experiment with new features
- Submit issues for questions
- Share improvements and suggestions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

For questions related to this Udemy course project:
- Review the code comments for explanations
- Check the FastAPI documentation: https://fastapi.tiangolo.com/
- Experiment with the code to understand concepts better

## 🎉 Acknowledgments

- FastAPI community for excellent documentation
- Udemy students for feedback and suggestions
- Open source contributors who make learning accessible

---

**Happy Learning! 🚀**

*This project demonstrates real-world FastAPI development practices in a beginner-friendly way. Use it as a foundation for building more complex applications.*