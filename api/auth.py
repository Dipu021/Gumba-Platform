from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database.database import get_db,Base,engine
from security.hash_password import hash_password
from schemas.auth import CreateUser
from models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from security.verify_password import verify_password
from security.oauth2 import create_token,verify_token

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register")
def register_user(user:CreateUser,db:Session=Depends(get_db)):
        hashed_password = hash_password(user.password_hash)
        # Create New User
        new_user = User(
                username = user.username,
                email = user.email,
                password_hash = hashed_password,
                role = "user"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id
    }

# @router.post("/login")
# def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
#         user = db.query(User).filter(User.username == form_data.username).first()
#         if not user or not verify_password(form_data.password,user.password_hash):
#                 raise HTTPException(
#                         status_code=401,
#                         detail="Invalid Username or Password"
#                 )
#         access_token = create_token({
#                 "sub":form_data.username
#         })
#         return{
#                 "Access Token":access_token,
#                 "Token Type":"bearer"
#         }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )

    access_token = create_token({
        "sub": form_data.username
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
