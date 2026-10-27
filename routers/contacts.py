from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal
from database import get_db
import auth
from rapidfuzz import fuzz
from itertools import combinations


router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/create", response_model=schemas.ContactOut)
def new_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = models.Contact(name=contact.name, email=contact.email, phone=contact.phone, company=contact.company, owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/all", response_model=list[schemas.ContactOut])
def all_contacts(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    query = db.query(models.Contact).filter(models.Contact.owner_id == current_user.id).all()
    return query

@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == current_user.id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_contact.name = contact.name
    db_contact.email = contact.email
    db_contact.phone = contact.phone
    db_contact.company = contact.company
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == current_user.id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": f"Contact {contact_id} deleted"}

@router.get("/find-duplicates")
def find_duplicates(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    contacts = db.query(models.Contact).filter(models.Contact.owner_id == current_user.id).all()
    duplicates = []
    for contact1, contact2 in combinations(contacts, 2):
        score = fuzz.ratio(contact1.name, contact2.name)
        if score >= 85:
            duplicates.append({
                "contact1": contact1.name,
                "contact2": contact2.name,
                "score": score
            })
    return duplicates

@router.post("/merge/{keep_id}/{remove_id}", response_model=schemas.ContactOut)
def merge_contacts(keep_id: int, remove_id: int,  db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    keep_contact = db.query(models.Contact).filter(models.Contact.id == keep_id, models.Contact.owner_id == current_user.id).first()
    remove_contact = db.query(models.Contact).filter(models.Contact.id == remove_id, models.Contact.owner_id == current_user.id).first()
    if keep_contact is None or remove_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if keep_contact.name is None:
        keep_contact.name = remove_contact.name
    if keep_contact.email is None:
        keep_contact.email = remove_contact.email
    if keep_contact.phone is None:
        keep_contact.phone = remove_contact.phone
    if keep_contact.company is None:
        keep_contact.company = remove_contact.company
    db.delete(remove_contact)
    db.commit()
    db.refresh(keep_contact)
    return keep_contact

