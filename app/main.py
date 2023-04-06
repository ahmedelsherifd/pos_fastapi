from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sales import crud, schemas
from datetime import datetime, timedelta
from . import models
from .database import SessionLocal, engine
from decimal import Decimal

middleware = [
    Middleware(RawContextMiddleware,
               plugins=(plugins.RequestIdPlugin(),
                        plugins.CorrelationIdPlugin()))
]

app = FastAPI(middleware=middleware)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_object_or_404(db, get, pk):
    try:
        return get(db, pk)
    except:
        raise HTTPException(status_code=404, detail="object not found")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        context.data["db"] = db
        yield db
    finally:
        db.close()


@app.post("/orders/", response_model=schemas.Order)
def create_order(data: schemas.OrderInput, db: Session = Depends(get_db)):

    instance = crud.create_order(db, **data.dict())
    return instance


@app.post("/customers/", response_model=schemas.Customer)
def create_customer(data: schemas.CustomerInput,
                    db: Session = Depends(get_db)):
    instance = crud.create_customer(db, **data.dict())
    return instance


@app.post("/products/", response_model=schemas.Product)
def create_customer(data: schemas.ProductInput, db: Session = Depends(get_db)):
    instance = crud.create_product(db, **data.dict())
    return instance


@app.post("/categories/", response_model=schemas.Category)
def create_customer(data: schemas.CategoryInput,
                    db: Session = Depends(get_db)):
    instance = crud.create_category(db, **data.dict())
    return instance


@app.get("/variants/", response_model=list[schemas.ProductVariant])
def get_variants(db: Session = Depends(get_db)):
    data = crud.get_variants(db)
    return data


@app.get("/categories/", response_model=list[schemas.Category])
def get_variants(db: Session = Depends(get_db)):
    data = crud.get_categories(db)
    return data


@app.get("/customers/", response_model=list[schemas.Customer])
def get_customers(db: Session = Depends(get_db)):
    data = crud.get_customers(db)
    return data


@app.get("/sales-by-items/", response_model=list[schemas.SaleByItem])
def get_sales_by_items(db: Session = Depends(get_db)):
    data = crud.get_sales_by_items(db)
    return data


@app.get("/total-payments/", response_model=list[schemas.TotalPayment])
def get_total_payments(db: Session = Depends(get_db)):
    data = crud.get_total_payments(db)
    return data


@app.get("/products/{pk}/", response_model=schemas.Product)
def get_product(pk: int, db: Session = Depends(get_db)):
    instance = get_object_or_404(db, crud.get_product, pk)
    return instance


@app.get("/customers/{pk}/", response_model=schemas.Customer)
def get_customer(pk: int, db: Session = Depends(get_db)):
    instance = get_object_or_404(db, crud.get_customer, pk)
    return instance


@app.get("/orders/{pk}/", response_model=schemas.Order)
def get_order(pk: int, db: Session = Depends(get_db)):
    instance = get_object_or_404(db, crud.get_order, pk)
    return instance


@app.get("/total-payments/node/", response_model=Decimal)
def get_total_payments_node(db: Session = Depends(get_db)):
    instance = crud.get_total_payments_node(db)
    return instance


@app.post("/token/", response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm,
                         Depends()],
    db: Session = Depends(get_db)
) -> schemas.Token:

    user = crud.authenticate_user(db,
                                  username=form_data.username,
                                  password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(data={"sub": user.username},
    #                                    expires_delta=access_token_expires)
    return {"access_token": "jabgfaegfk", "token_type": "bearer"}
