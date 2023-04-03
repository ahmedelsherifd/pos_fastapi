from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sales import crud, schemas

from . import models
from .database import SessionLocal, engine

middleware = [
    Middleware(RawContextMiddleware,
               plugins=(plugins.RequestIdPlugin(),
                        plugins.CorrelationIdPlugin()))
]

app = FastAPI(middleware=middleware)


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
