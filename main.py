from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr
import json
import os

# App Configuration


app = FastAPI(title="FastAPI JWT Authentication")

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
DATABASE = "users.json"

security = HTTPBearer()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# JSON Functions


def read_users():

    if not os.path.exists(DATABASE):
        with open(DATABASE, "w") as file:
            json.dump([], file)

    try:
        with open(DATABASE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_users(users):

    with open(DATABASE, "w") as file:
        json.dump(users, file, indent=4)


# Models

class Signup(BaseModel):
    username: str
    email: EmailStr
    password: str


class Login(BaseModel):
    username: str
    password: str


# JWT Functions

def create_token(username: str):

    payload = {
        "sub": username
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )


# Home Page


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Signup

@app.post("/signup")
def signup(user: Signup):

    users = read_users()

    # Check username

    for u in users:

        if u["username"] == user.username:

            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

    # Check email

    for u in users:

        if u["email"] == user.email:

            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    users.append(
        {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "token": ""
        }
    )

    save_users(users)

    return {
        "message": "Signup Successful"
    }
    
# Login


@app.post("/login")
def login(user: Login):

    users = read_users()

    for u in users:

        if u["username"] == user.username:

            if u["password"] != user.password:
                raise HTTPException(
                    status_code=400,
                    detail="Incorrect Password"
                )

            # Generate JWT Token
            token = create_token(user.username)

            # Save Token in JSON
            u["token"] = token

            save_users(users)

            return {
                "message": "Login Successful",
                "token": token
            }

    raise HTTPException(
        status_code=404,
        detail="User not found. Please Sign Up first."
    )


# Profile


@app.get("/profile")
def profile(current_user=Depends(verify_token)):

    users = read_users()

    for user in users:

        if user["username"] == current_user:

            return {
                "username": user["username"],
                "email": user["email"]
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# Get All Users


@app.get("/users")
def get_users():

    return read_users()


# Delete Current User


@app.delete("/delete")
def delete_user(current_user=Depends(verify_token)):

    users = read_users()

    updated_users = []

    found = False

    for user in users:

        if user["username"] == current_user:

            found = True

        else:

            updated_users.append(user)

    if not found:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    save_users(updated_users)

    return {
        "message": "Account Deleted Successfully"
    }



# Logout

@app.post("/logout")
def logout(current_user=Depends(verify_token)):

    users = read_users()

    for user in users:

        if user["username"] == current_user:

            user["token"] = ""

    save_users(users)

    return {
        "message": "Logout Successful"
    }