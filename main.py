from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from config import settings
from routers import pomodoros, projects, recall_projects, recalls, users, categories

templates = Jinja2Templates(directory="templates")

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(projects.router)
app.include_router(pomodoros.router)
app.include_router(recall_projects.router)
app.include_router(recalls.router)


@app.get("/", include_in_schema=False)
def home(request: Request, msg:str = None):
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "msg":msg}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)