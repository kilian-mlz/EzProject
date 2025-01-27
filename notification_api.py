from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Notification(BaseModel):
    email: str
    ticket_name: str
    ticket_status: str


@app.put("/v1/notify-user", status_code=202)
async def notify_user(notification: Notification):
    if not all([notification.email, notification.ticket_name, notification.ticket_status]):
        raise HTTPException(status_code=400, detail="All fields are required")

    try:
        message = f"""
        ----------------------------------------
        NOTIFICATION: Ticket Status Update
        ----------------------------------------
        To: {notification.email}
        Ticket Name: {notification.ticket_name}
        Current Status: {notification.ticket_status}

        We wanted to inform you that the status of your ticket 
        '{notification.ticket_name}' has been updated to '{notification.ticket_status}'.

        ----------------------------------------
        
        """

        with open("notifications.txt", "a") as file:
            file.write(message)

        return {"detail": "Notification sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send notification")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8082)
