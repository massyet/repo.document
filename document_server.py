from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

# Configura cartelle
app.mount("/documents", StaticFiles(directory="documents"), name="documents")
templates = Jinja2Templates(directory="templates")

# Carica le email autorizzate
with open("authorized_emails.json", "r") as f:
    authorized_emails = json.load(f)["emails"]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "error": False})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...)):
    if email.lower() in authorized_emails:
        files = os.listdir("documents")
        return templates.TemplateResponse("files.html", {"request": request, "files": files})
    return templates.TemplateResponse("index.html", {"request": request, "error": True})

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("documents", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    return RedirectResponse(url="/")
