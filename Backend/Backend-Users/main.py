from database import (
    fetch_all_users,
    fetch_one_user,
    create_user,
    update_user,
    remove_user,
    fetch_one_user_by_username,
)

from utils import (
    get_current_active_user,
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from datetime import timedelta
from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Body,
    Depends,
    Response,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm


from model import User, UserInDb, UpdateUserModel, Token, TokenData
import os
from dotenv import load_dotenv


load_dotenv()


access_token_expire_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Tokens
@app.post("/token", response_model=Token, tags=["Tokens"])
async def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"access_token": access_token, "token_type": "bearer"}


# Account Verification #Get Personal Account Details
@app.get("/accounts/profile", response_model=User, tags=["User Authentication"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/accounts/profile/items", tags=["User Authentication"])
async def read_own_items(
    response: Response, current_user: User = Depends(get_current_active_user)
):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"todos": current_user.todos, "categories": current_user.categories}


# User CRUD
@app.get("/api/user", tags=["CRUD Users"])
async def get_users():
    response = await fetch_all_users()
    return response


@app.post(
    "/api/user",
    response_description="Add a new user",
    response_model=User,
    tags=["CRUD Users"],
)
async def post_user(user: UserInDb = Body(...)):
    existing_user = await fetch_one_user_by_username(user.username)
    if existing_user:
        raise HTTPException(400, "Username already exists")
    else:
        user.username = user.username.lower()
        user.hashed_password = get_password_hash(user.hashed_password)
        user = jsonable_encoder(user)
        response = await create_user(user)
        if response:
            return response
        raise HTTPException(400, "Something went wrong / Bad Request")


@app.get(
    "/api/user/{id}",
    response_description="Get a single user",
    response_model=User,
    tags=["CRUD Users"],
)
async def get_user_by_id(id: str):
    response = await fetch_one_user(id)
    if response:
        return response
    raise HTTPException(404, f"ID {id} not found")


@app.get(
    "/api/user/username/{username}",
    response_description="Get a single user by username",
    response_model=UserInDb,
    tags=["CRUD Users"],
)
async def get_user_by_username(username: str):
    response = await fetch_one_user_by_username(username)
    if response:
        return response
    raise HTTPException(404, f"{username} not found")


@app.put(
    "/api/user/{id}",
    response_description="Update a user",
    response_model=User,
    tags=["CRUD Users"],
)
async def put_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    user["hashed_password"] = get_password_hash(user["hashed_password"])
    if len(user) >= 1:
        response = await update_user(id, user)
    if response:
        return response
    raise HTTPException(404, f"There is no user account with this {id}")


@app.delete("/api/user/{id}", response_description="Delete a user", tags=["CRUD Users"])
async def delete_user(id: str):
    response = await remove_user(id)
    if response:
        return "Successfully deleted user item"
    raise HTTPException(404, f"There is no TODO item with this id:{id}")


# Users End
