"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Example schemas (you can keep these for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Zorgkwekerij - Collections

class ClientApplication(BaseModel):
    """Applications from clients interested in day activities"""
    first_name: str = Field(..., description="Voornaam")
    last_name: str = Field(..., description="Achternaam")
    email: Optional[EmailStr] = Field(None, description="E-mailadres")
    phone: Optional[str] = Field(None, description="Telefoonnummer")
    date_of_birth: Optional[str] = Field(None, description="Geboortedatum (YYYY-MM-DD)")
    support_needs: Optional[str] = Field(None, description="Ondersteuningsbehoeften")
    preferred_days: Optional[str] = Field(None, description="Voorkeursdagen")
    message: Optional[str] = Field(None, description="Aanvullende informatie")

class PartnerInquiry(BaseModel):
    """Inquiries from professional care providers and partners"""
    organization: str = Field(..., description="Organisatienaam")
    contact_name: str = Field(..., description="Contactpersoon")
    email: EmailStr = Field(..., description="E-mailadres")
    phone: Optional[str] = Field(None, description="Telefoonnummer")
    referral_process_stage: Optional[str] = Field(None, description="Fase in het verwijsproces")
    target_group: Optional[str] = Field(None, description="Doelgroep / indicatie")
    message: Optional[str] = Field(None, description="Vraag / Opmerking")

class VolunteerApplication(BaseModel):
    """Applications from volunteers"""
    name: str = Field(..., description="Naam")
    email: Optional[EmailStr] = Field(None, description="E-mailadres")
    phone: Optional[str] = Field(None, description="Telefoonnummer")
    interests: Optional[str] = Field(None, description="Interesses / Voorkeursrollen")
    availability: Optional[str] = Field(None, description="Beschikbaarheid")
    motivation: Optional[str] = Field(None, description="Motivatie")

class ContactMessage(BaseModel):
    """General contact messages"""
    name: str = Field(..., description="Naam")
    email: Optional[EmailStr] = Field(None, description="E-mailadres")
    phone: Optional[str] = Field(None, description="Telefoonnummer")
    subject: Optional[str] = Field(None, description="Onderwerp")
    message: str = Field(..., description="Bericht")

# Note: The Flames database viewer can read schemas from the /schema endpoint if implemented.
