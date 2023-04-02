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


@app.get("/variants/")
def get_variants(db: Session = Depends(get_db)):
    variants = crud.get_variants(db)
    return variants


@app.post("/orders/")
def create_order(order: schemas.OrderInput, db: Session = Depends(get_db)):

    instance = crud.create_order(db, **order.dict())
    return {}
