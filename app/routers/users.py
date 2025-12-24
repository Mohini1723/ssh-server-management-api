from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserInDB, UserProfileUpdate
from app.database import db
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserInDB)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    update_data = {k: v for k, v in profile_data.dict().items() if v is not None}
    
    if update_data:
        await db.users.update_one(
            {"email": current_user.email},
            {"$set": update_data}
        )
      
        updated_user = await db.users.find_one({"email": current_user.email})
        return UserInDB(**updated_user)
    
    return current_user

@router.delete("/me")
async def delete_user_account(current_user: UserInDB = Depends(get_current_user)):
    await db.users.delete_one({"email": current_user.email})
    return {"message": "Account deleted successfully"}
