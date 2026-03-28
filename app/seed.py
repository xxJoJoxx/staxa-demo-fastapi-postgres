from sqlalchemy.orm import Session

from app.models import Contact


SAMPLE_CONTACTS = [
    {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "555-0101",
        "notes": "Met at the tech conference in March.",
    },
    {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "phone": "555-0102",
        "notes": "Project collaborator on the API redesign.",
    },
    {
        "name": "Carol Williams",
        "email": "carol@example.com",
        "phone": "555-0103",
        "notes": "Frontend lead on the dashboard project.",
    },
]


def seed_contacts(db: Session) -> None:
    if db.query(Contact).count() > 0:
        return
    for data in SAMPLE_CONTACTS:
        db.add(Contact(**data))
    db.commit()
