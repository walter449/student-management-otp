from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from database import engine, Base
from routes import students, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(auth.router)

# Archivos estáticos
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# Página principal → Login
@app.get("/")
def login_page():
    return FileResponse("frontend/login.html")


# Página principal del sistema después del login
@app.get("/index")
def index_page():
    return FileResponse("frontend/index.html")

