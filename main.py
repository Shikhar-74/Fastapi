from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.mydatabase
collection = db.mycollection

class FormData(BaseModel):
    name: str
    email: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <head>
            <title>Form</title>
        </head>
        <body>
            <form action="/submit" method="post">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name"><br><br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email"><br><br>
                <label for="message">Message:</label>
                <textarea id="message" name="message"></textarea><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

@app.post("/submit")
async def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    form_data = FormData(name=name, email=email, message=message)
    collection.insert_one(form_data.dict())
    return {"message": "Form submitted successfully"}
