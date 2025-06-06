from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from api.routes.routes import home_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(home_router)
register_tortoise(
    app=app,
    db_url="sqlite://home.db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models": ["api.models.models"]},
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/bookings/{email}", response_class=HTMLResponse)
async def view_bookings(request: Request, email: str):
    return templates.TemplateResponse(
        "bookings.html",
        {"request": request, "email": email}
    )