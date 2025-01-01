from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import create_tables
from app.models import Subscription, Subscriber
from app.database import SessionLocal

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    subjects = ["Technology", "Health", "Finance", "Sports", "Entertainment"]  # Placeholder
    return templates.TemplateResponse("home.html", {"request": request, "subjects": subjects})

@app.post("/", response_class=HTMLResponse)
def handle_subscription(
    request: Request, 
    email: str = Form(...), 
    action: str = Form(...), 
    subjects: list[str] = Form([])
):
    db = SessionLocal()
    if action == "subscribe":
        existing_subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
        if existing_subscriber:
            db.query(Subscription).filter(Subscription.subscriber_id == existing_subscriber.id).delete()
            for subject in subjects:
                new_subscription = Subscription(subject=subject, subscriber_id=existing_subscriber.id)
                db.add(new_subscription)
            db.commit()
            db.close()
            return templates.TemplateResponse(
                "home.html",
                {
                    "request": request,
                    "success": "Your subscription preferences have been updated!",
                    "subjects": [],
                    "subscribed": True,
                    "process_complete": True,
                }
            )
        new_subscriber = Subscriber(email=email)
        db.add(new_subscriber)
        db.commit()
        db.refresh(new_subscriber)

        for subject in subjects:
            subscription = Subscription(subject=subject, subscriber_id=new_subscriber.id)
            db.add(subscription)
        db.commit()
        db.close()

        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "success": "You have successfully subscribed!",
                "subjects": [],
                "subscribed": True,
                "process_complete": True,
            }
        )

    elif action == "unsubscribe":
        existing_subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
        if not existing_subscriber:
            db.close()
            return templates.TemplateResponse(
                "home.html",
                {
                    "request": request,
                    "error": "Email not found in our database!",
                    "subjects": [],
                    "subscribed": False,
                    "process_complete": True,
                }
            )
        db.query(Subscription).filter(Subscription.subscriber_id == existing_subscriber.id).delete()
        db.delete(existing_subscriber)
        db.commit()
        db.close()

        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "success": "You have successfully unsubscribed from our newsletter.",
                "subjects": [],
                "subscribed": False,
                "process_complete": True,
            }
        )
