import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contact

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate(name: str, email: str) -> list[str]:
    errors = []
    if not name or not name.strip():
        errors.append("Name is required.")
    if not email or not email.strip():
        errors.append("Email is required.")
    elif not EMAIL_RE.match(email):
        errors.append("Email must be a valid email address.")
    return errors


def _render(name: str, request: Request, context: dict):
    return templates.TemplateResponse(request, name, context)


@router.get("/")
def contact_list(request: Request, db: Session = Depends(get_db)):
    contacts = db.query(Contact).order_by(Contact.id).all()
    message = request.query_params.get("message")
    return _render("list.html", request, {"contacts": contacts, "message": message})


@router.get("/contacts/new")
def new_contact_form(request: Request):
    return _render("form.html", request, {"contact": None, "errors": []})


@router.post("/contacts/new")
def create_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    errors = _validate(name, email)
    if errors:
        return _render("form.html", request, {
            "contact": {"name": name, "email": email, "phone": phone, "notes": notes},
            "errors": errors,
        })
    contact = Contact(name=name.strip(), email=email.strip(), phone=phone.strip() or None, notes=notes.strip() or None)
    db.add(contact)
    db.commit()
    return RedirectResponse(url="/?message=Contact+created+successfully", status_code=303)


@router.get("/contacts/{contact_id}")
def view_contact(request: Request, contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return RedirectResponse(url="/?message=Contact+not+found", status_code=303)
    return _render("detail.html", request, {"contact": contact})


@router.get("/contacts/{contact_id}/edit")
def edit_contact_form(request: Request, contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return RedirectResponse(url="/?message=Contact+not+found", status_code=303)
    return _render("form.html", request, {"contact": contact, "errors": []})


@router.post("/contacts/{contact_id}/edit")
def update_contact(
    request: Request,
    contact_id: int,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return RedirectResponse(url="/?message=Contact+not+found", status_code=303)

    errors = _validate(name, email)
    if errors:
        return _render("form.html", request, {
            "contact": {"id": contact_id, "name": name, "email": email, "phone": phone, "notes": notes},
            "errors": errors,
        })

    contact.name = name.strip()
    contact.email = email.strip()
    contact.phone = phone.strip() or None
    contact.notes = notes.strip() or None
    db.commit()
    return RedirectResponse(url=f"/contacts/{contact_id}?message=Contact+updated+successfully", status_code=303)


@router.post("/contacts/{contact_id}/delete")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return RedirectResponse(url="/?message=Contact+deleted+successfully", status_code=303)
