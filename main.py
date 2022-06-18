from fastapi import FastAPI

from routers import pomodoros, projects, recall_projects, recalls, users, categories
from data import Database

DB = Database()

app = FastAPI()
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(projects.router)
app.include_router(pomodoros.router)
app.include_router(recall_projects.router)
app.include_router(recalls.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)