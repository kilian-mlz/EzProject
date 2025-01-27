from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import requests
from models import Ticket, StatusEnum, User
from database import get_db

app = FastAPI()

class TicketCreate(BaseModel):
    name: str
    description: str
    user_id: int

class TicketUpdate(BaseModel):
    status: StatusEnum

class TicketResponse(BaseModel):
    id: int
    name: str
    description: str
    status: StatusEnum
    user_id: int

    class Config:
        from_attributes = True


@app.post("/v1/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    if not requests.get(f"http://127.0.0.1:8081/v1/users/{ticket.user_id}").ok:
        raise HTTPException(status_code=400, detail="Invalid user")
    db_ticket = Ticket(**ticket.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@app.get("/v1/tickets", response_model=list[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()


@app.get("/v1/tickets/{id}", response_model=TicketResponse)
def get_ticket(id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


def is_valid_transition(current_status, new_status):
    VALID_TRANSITIONS = {
        "TODO": ["IN_PROGRESS"],
        "IN_PROGRESS": ["DONE"],
        "DONE": []
    }

    return new_status in VALID_TRANSITIONS.get(current_status, [])


NOTIFICATION_API_URL = "http://127.0.0.1:8082/v1/notify-user"

@app.put("/v1/tickets/{id}", response_model=TicketResponse)
def update_ticket(id: int, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    current_status = db_ticket.status.value
    new_status = ticket_update.status.value

    if not is_valid_transition(current_status, new_status):
        raise HTTPException(status_code=400, detail="Invalid status transition")

    db_ticket.status = ticket_update.status
    db.commit()
    db.refresh(db_ticket)

    user = db.query(User).filter(User.id == db_ticket.user_id).first()
    if user:
        notification_data = {
            "email": user.email,
            "ticket_name": db_ticket.name,
            "ticket_status": new_status
        }
        response = requests.put(NOTIFICATION_API_URL, json=notification_data)
        if response.status_code != 202:
            raise HTTPException(status_code=500, detail="Failed to send notification")

    return db_ticket


@app.delete("/v1/tickets/{id}")
def delete_ticket(id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(db_ticket)
    db.commit()
    return {"detail": "Ticket deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8083)
