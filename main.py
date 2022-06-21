from fastapi import FastAPI

from config import settings
from data import Database
from routers import pomodoros, projects, recall_projects, recalls, users, categories


DB = Database()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(projects.router)
app.include_router(pomodoros.router)
app.include_router(recall_projects.router)
app.include_router(recalls.router)


# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")


# templates = Jinja2Templates(directory="templates")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     print(request)
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)