"""
Event Registration Form - FastAPI Application

A web application for event registration with email verification.
Built for educational purposes as part of a Udemy course on FastAPI.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

import config
from models import (
    EventRegistration, 
    VerificationRequest, 
    PendingRegistration, 
    RegistrationResponse, 
    VerificationResponse
)
from email_service import send_verification_email, generate_verification_code

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version="1.0.0"
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for pending registrations
# In production, use a proper database like PostgreSQL or MongoDB
pending_registrations: Dict[str, PendingRegistration] = {}

# In-memory storage for completed registrations
completed_registrations: Dict[str, dict] = {}


@app.get("/", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    """Display the event registration form."""
    return templates.TemplateResponse("registration_form.html", {
        "request": request,
        "events": config.AVAILABLE_EVENTS,
        "app_name": config.APP_NAME
    })


@app.post("/register")
async def register_for_event(
    request: Request,
    name: str = Form(...),
    email: str = Form(...), 
    event_id: str = Form(...)
):
    """
    Process event registration and send verification email.
    """
    try:
        # Validate the registration data
        registration = EventRegistration(name=name, email=email, event_id=event_id)
        
        # Check if email is already registered for this event
        if email in completed_registrations:
            return templates.TemplateResponse("registration_form.html", {
                "request": request,
                "events": config.AVAILABLE_EVENTS,
                "app_name": config.APP_NAME,
                "error": "This email is already registered. Please use a different email address.",
                "form_data": {"name": name, "email": email, "event_id": event_id}
            })
        
        # Generate verification code
        verification_code = generate_verification_code()
        
        # Get event details
        event = next((e for e in config.AVAILABLE_EVENTS if e['id'] == event_id), None)
        if not event:
            raise HTTPException(status_code=400, detail="Invalid event selection")
        
        # Create pending registration
        expires_at = datetime.now() + timedelta(minutes=config.VERIFICATION_CODE_EXPIRY_MINUTES)
        pending_registration = PendingRegistration(
            name=registration.name,
            email=registration.email,
            event_id=registration.event_id,
            verification_code=verification_code,
            created_at=datetime.now(),
            expires_at=expires_at
        )
        
        # Store pending registration
        pending_registrations[email] = pending_registration
        
        # Send verification email
        email_sent = await send_verification_email(
            recipient_email=email,
            verification_code=verification_code,
            name=registration.name,
            event_name=event['name']
        )
        
        if not email_sent:
            return templates.TemplateResponse("registration_form.html", {
                "request": request,
                "events": config.AVAILABLE_EVENTS,
                "app_name": config.APP_NAME,
                "error": "Failed to send verification email. Please try again.",
                "form_data": {"name": name, "email": email, "event_id": event_id}
            })
        
        # Redirect to verification page
        return RedirectResponse(url=f"/verify?email={email}", status_code=303)
        
    except ValueError as e:
        return templates.TemplateResponse("registration_form.html", {
            "request": request,
            "events": config.AVAILABLE_EVENTS,
            "app_name": config.APP_NAME,
            "error": str(e),
            "form_data": {"name": name, "email": email, "event_id": event_id}
        })
    except Exception as e:
        return templates.TemplateResponse("registration_form.html", {
            "request": request,
            "events": config.AVAILABLE_EVENTS,
            "app_name": config.APP_NAME,
            "error": "An unexpected error occurred. Please try again.",
            "form_data": {"name": name, "email": email, "event_id": event_id}
        })


@app.get("/verify", response_class=HTMLResponse)
async def show_verification_form(request: Request, email: str):
    """Display the email verification form."""
    # Check if there's a pending registration for this email
    if email not in pending_registrations:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "app_name": config.APP_NAME,
            "error": "No pending registration found for this email address.",
            "back_url": "/"
        })
    
    pending_reg = pending_registrations[email]
    
    # Check if verification code has expired
    if datetime.now() > pending_reg.expires_at:
        del pending_registrations[email]
        return templates.TemplateResponse("error.html", {
            "request": request,
            "app_name": config.APP_NAME,
            "error": "Verification code has expired. Please register again.",
            "back_url": "/"
        })
    
    return templates.TemplateResponse("verification_form.html", {
        "request": request,
        "app_name": config.APP_NAME,
        "email": email,
        "name": pending_reg.name
    })


@app.post("/verify")
async def verify_registration(
    request: Request,
    email: str = Form(...),
    verification_code: str = Form(...)
):
    """
    Verify the registration with the provided code.
    """
    try:
        # Validate the verification request
        verification = VerificationRequest(email=email, verification_code=verification_code)
        
        # Check if there's a pending registration
        if email not in pending_registrations:
            return templates.TemplateResponse("verification_form.html", {
                "request": request,
                "app_name": config.APP_NAME,
                "email": email,
                "error": "No pending registration found for this email address."
            })
        
        pending_reg = pending_registrations[email]
        
        # Check if verification code has expired
        if datetime.now() > pending_reg.expires_at:
            del pending_registrations[email]
            return templates.TemplateResponse("verification_form.html", {
                "request": request,
                "app_name": config.APP_NAME,
                "email": email,
                "error": "Verification code has expired. Please register again."
            })
        
        # Check if verification code matches
        if verification_code != pending_reg.verification_code:
            return templates.TemplateResponse("verification_form.html", {
                "request": request,
                "app_name": config.APP_NAME,
                "email": email,
                "name": pending_reg.name,
                "error": "Invalid verification code. Please try again."
            })
        
        # Registration successful - move to completed registrations
        event = next((e for e in config.AVAILABLE_EVENTS if e['id'] == pending_reg.event_id), None)
        completed_registrations[email] = {
            "name": pending_reg.name,
            "email": pending_reg.email,
            "event": event,
            "registered_at": datetime.now()
        }
        
        # Remove from pending registrations
        del pending_registrations[email]
        
        # Redirect to success page
        return RedirectResponse(url=f"/success?email={email}", status_code=303)
        
    except ValueError as e:
        return templates.TemplateResponse("verification_form.html", {
            "request": request,
            "app_name": config.APP_NAME,
            "email": email,
            "error": str(e)
        })
    except Exception as e:
        return templates.TemplateResponse("verification_form.html", {
            "request": request,
            "app_name": config.APP_NAME,
            "email": email,
            "error": "An unexpected error occurred. Please try again."
        })


@app.get("/success", response_class=HTMLResponse)
async def show_success_page(request: Request, email: str):
    """Display the registration success page."""
    # Check if registration exists
    if email not in completed_registrations:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "app_name": config.APP_NAME,
            "error": "Registration not found.",
            "back_url": "/"
        })
    
    registration = completed_registrations[email]
    
    return templates.TemplateResponse("success.html", {
        "request": request,
        "app_name": config.APP_NAME,
        "registration": registration
    })


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app_name": config.APP_NAME,
        "timestamp": datetime.now().isoformat()
    }


# For development purposes - view registered users
@app.get("/admin/registrations")
async def view_registrations():
    """
    Admin endpoint to view all registrations.
    Note: In production, this should be protected with authentication.
    """
    return {
        "completed_registrations": len(completed_registrations),
        "pending_registrations": len(pending_registrations),
        "registrations": list(completed_registrations.values())
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )