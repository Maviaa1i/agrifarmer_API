import io

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.database import Base, engine, get_db
from app.model_loader import predict_image
from app.models import User
from app.schemas import Token, UserCreate, UserOut
from app.suggestions import get_suggestion

# Tables automatically ban jayengi (pehli baar chalne par)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wheat Disease Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Wheat Disease Detection API is running"}


# ---------------- AUTH ----------------
@app.post("/auth/register", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")

    user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return Token(access_token=create_access_token(user.username))


@app.get("/auth/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


# ---------------- PREDICTION (protected) ----------------
@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

    predicted_class, confidence = predict_image(image)
    info = get_suggestion(predicted_class)

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "disease_name": info["disease_name"],
        "severity": info["severity"],
        "description": info["description"],
        "recommendation": info["recommendation"],
    }