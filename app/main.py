from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.aws_dynamodb import add_user, update_user_topics, get_user_by_email, delete_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup():
    # You may want to ensure that your DynamoDB table is created before handling requests
    pass

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
    if action == "subscribe":
        # Check if the user already exists in DynamoDB
        existing_user = get_user_by_email(email)
        if existing_user:
            # Update the user's subscription topics in DynamoDB
            update_user_topics(email, subjects)
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
        
        # If the user does not exist, add them to DynamoDB
        add_user(email, subjects)
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
        existing_user = get_user_by_email(email)
        if not existing_user:
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
        # Remove user from subscriptions and delete from DynamoDB
        delete_user(email)
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
