import json
from fastapi import FastAPI, Form, Query
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
    
    # Search criteria based on email to prevent duplicates
    query = {"email": email}
    
    # Update or insert based on the email
    collection.update_one(
        query,                           # Search criteria based on email
        {"$set": form_data.dict()},      # Update the document with new data
        upsert=True                      # Insert a new document if no match is found
    )
    
    return {"message": "Form submitted successfully"}

@app.get("/get-user-data")
async def get_user_data(email: str = Query(...)):
    # Search for the document by email
    user_data = collection.find_one({"email": email})
    
    # If user is found, return the data; otherwise, return a not found message
    if user_data:
        user_data["_id"] = str(user_data["_id"])
        return user_data
    else:
        return {"message": "User not found"}

# Function to get user data from terminal input and display in JSON format
def get_user_data_from_terminal():
    email = input("Enter the email ID to search: ")
    
    # Search for the document by email
    user_data = collection.find_one({"email": email})
    
    if user_data:
        # Convert ObjectId to string and format the data as JSON
        user_data["_id"] = str(user_data["_id"])
        print(json.dumps(user_data, indent=4))  # Pretty-printing the JSON data
    else:
        print(json.dumps({"message": "User not found"}, indent=4))

# Run the function only if this file is executed directly
if __name__ == "__main__":
    get_user_data_from_terminal()
