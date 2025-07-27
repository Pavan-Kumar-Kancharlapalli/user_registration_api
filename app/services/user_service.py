from app.data.db import user_collection, token_collection
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_access_token
from datetime import datetime, timedelta
from fastapi import HTTPException
import uuid


def register_user(data):
    existing_user = user_collection.find_one({"username": data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pwd = hash_password(data.password)
    user_doc = {
        "username": data.username,
        "password": hashed_pwd,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "address": data.address,
        "created_at": datetime.utcnow()
    }
    user_collection.insert_one(user_doc)
    return {"message": "User registered successfully", "status": "success"}


def login_user(data):
    user = user_collection.find_one({"username": data.username})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": data.username}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}


def change_password(username, old_pwd, new_pwd):
    user = user_collection.find_one({"username": username})
    if not user or not verify_password(old_pwd, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid current password")

    if verify_password(new_pwd, user["password"]):
        raise HTTPException(status_code=400, detail="New password cannot be same as old password")

    hashed_new = hash_password(new_pwd)
    user_collection.update_one({"username": username}, {"$set": {"password": hashed_new}})
    return {"message": "Password changed successfully", "status": "success"}


def forget_password(username):
    user = user_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    request_count = token_collection.count_documents({"username": username, "created_at": {"$gte": datetime.utcnow() - timedelta(hours=24)}})
    if request_count >= 3:
        raise HTTPException(status_code=429, detail="Too many reset requests. Try after 24 hours.")

    token = str(uuid.uuid4())
    token_collection.insert_one({
        "username": username,
        "token": token,
        "created_at": datetime.utcnow()
    })

    # In production, send this via email.
    return {"message": "Password reset token generated", "token": token, "status": "success"}


def reset_password(token, new_password):
    token_entry = token_collection.find_one({"token": token})
    if not token_entry:
        raise HTTPException(status_code=404, detail="Invalid token")

    if datetime.utcnow() - token_entry["created_at"] > timedelta(hours=24):
        raise HTTPException(status_code=410, detail="Token expired")

    user_collection.update_one(
        {"username": token_entry["username"]},
        {"$set": {"password": hash_password(new_password)}}
    )

    token_collection.delete_one({"token": token})
    return {"message": "Password reset successfully", "status": "success"}



def logout_user(token: str):
    from app.data.db import token_collection
    from datetime import datetime

    token_collection.insert_one({
        "token": token,
        "blacklisted_at": datetime.utcnow()
    })
    return {"message": "User logged out successfully"}
