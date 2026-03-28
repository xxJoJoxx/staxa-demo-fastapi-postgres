from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class ContactBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    notes: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
