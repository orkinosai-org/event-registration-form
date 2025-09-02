"""
Pydantic models for the Event Registration Form application.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class EventRegistration(BaseModel):
    """Model for event registration form data."""
    name: str
    email: EmailStr
    event_id: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('event_id')
    def event_id_must_be_valid(cls, v):
        from config import AVAILABLE_EVENTS
        valid_event_ids = [event['id'] for event in AVAILABLE_EVENTS]
        if v not in valid_event_ids:
            raise ValueError(f'Invalid event selection. Must be one of: {valid_event_ids}')
        return v


class VerificationRequest(BaseModel):
    """Model for email verification request."""
    email: EmailStr
    verification_code: str
    
    @validator('verification_code')
    def code_must_be_six_digits(cls, v):
        if not v or len(v) != 6 or not v.isdigit():
            raise ValueError('Verification code must be exactly 6 digits')
        return v


class PendingRegistration(BaseModel):
    """Model for storing pending registrations awaiting verification."""
    name: str
    email: EmailStr
    event_id: str
    verification_code: str
    created_at: datetime
    expires_at: datetime
    verified: bool = False
    
    class Config:
        # Allow datetime objects to be serialized
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RegistrationResponse(BaseModel):
    """Model for registration API response."""
    success: bool
    message: str
    email: Optional[str] = None


class VerificationResponse(BaseModel):
    """Model for verification API response."""
    success: bool
    message: str
    registration_complete: bool = False