import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import ClientApplication, PartnerInquiry, VolunteerApplication, ContactMessage

app = FastAPI(title="Zorgkwekerij Plant en Tuin Noordbroek API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Zorgkwekerij API running"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response: Dict[str, Any] = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "❓"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# Helper to insert into collection following schema naming (class name -> lowercased collection)

def _insert_model(model: BaseModel):
    collection = model.__class__.__name__.lower()
    data = model.dict()
    created = create_document(collection, data)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create document")
    return {"success": True, "id": str(created.get("_id"))}

# Public endpoints used by frontend forms

@app.post("/api/applications/clients")
def submit_client_application(payload: ClientApplication):
    return _insert_model(payload)

@app.post("/api/inquiries/partners")
def submit_partner_inquiry(payload: PartnerInquiry):
    return _insert_model(payload)

@app.post("/api/applications/volunteers")

def submit_volunteer_application(payload: VolunteerApplication):
    return _insert_model(payload)

@app.post("/api/contact")

def submit_contact_message(payload: ContactMessage):
    return _insert_model(payload)

# Simple read endpoints (latest submissions)

@app.get("/api/submissions/{collection}")

def get_latest_submissions(collection: str, limit: int = 10):
    allowed = {"clientapplication", "partnerinquiry", "volunteerapplication", "contactmessage"}
    if collection not in allowed:
        raise HTTPException(status_code=400, detail="Invalid collection")
    docs = get_documents(collection, filter_dict={}, limit=limit)
    return {"items": docs}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
