from fastapi import FastAPI, HTTPException, Path, Query
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column
)
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing in .env file")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column()
    category: Mapped[str] = mapped_column(String(100))


app = FastAPI()

Base.metadata.create_all(bind=engine)


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=100)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    price: float | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, min_length=2, max_length=100)


@app.post("/products", response_model=ProductResponse)
def create_product(product_data: ProductCreate):
    db = SessionLocal()

    try:
        new_product = Product(
            name=product_data.name,
            price=product_data.price,
            category=product_data.category
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product

    finally:
        db.close()


@app.get("/products/", response_model=list[ProductResponse])
def get_all_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1)
):
    db = SessionLocal()

    try:
        query = select(Product).offset(skip).limit(limit)
        result = db.execute(query)
        products = result.scalars().all()

        return products

    finally:
        db.close()


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int = Path(ge=1)):
    db = SessionLocal()

    try:
        query = select(Product).where(Product.id == product_id)
        result = db.execute(query)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product

    finally:
        db.close()


@app.put("/products/{product_id}", response_model=ProductResponse)
def replace_product(product_id: int, product_data: ProductCreate):
    db = SessionLocal()

    try:
        query = select(Product).where(Product.id == product_id)
        product = db.execute(query).scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product.name = product_data.name
        product.price = product_data.price
        product.category = product_data.category

        db.commit()
        db.refresh(product)

        return product

    finally:
        db.close()


@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate):
    db = SessionLocal()

    try:
        query = select(Product).where(Product.id == product_id)
        product = db.execute(query).scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product_data.name is not None:
            product.name = product_data.name

        if product_data.price is not None:
            product.price = product_data.price

        if product_data.category is not None:
            product.category = product_data.category

        db.commit()
        db.refresh(product)

        return product

    finally:
        db.close()


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()

    try:
        query = select(Product).where(Product.id == product_id)
        product = db.execute(query).scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        db.delete(product)
        db.commit()

        return {"message": "Product deleted successfully"}

    finally:
        db.close()




@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate):
    db = SessionLocal()

    try:
        query = select(Product).where(Product.id == product_id)
        product = db.execute(query).scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product_data.name is not None:
            product.name = product_data.name

        if product_data.price is not None:
            product.price = product_data.price

        if product_data.category is not None:
            product.category = product_data.category

        db.commit()
        db.refresh(product)

        return product

    finally:
        db.close()
