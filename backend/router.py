from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product,
)

router = APIRouter()


@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    """
    A route function to create a product, using the provided product data and database session.
    Parameters:
        - product: ProductCreate
        - db: Session
    Returns:
        - ProductResponse
    """
    return create_product(db=db, product=product)


@router.get("/products/", response_model=List[ProductResponse])
def read_all_products_route(db: Session = Depends(get_db)):
    """
    Get all products from the database.

    Parameters:
        db (Session): The database session.

    Returns:
        List[ProductResponse]: A list of product responses.
    """
    products = get_products(db)
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    """
    A route to read a specific product identified by product_id.
    
    Parameters:
        - product_id: an integer representing the ID of the product to retrieve.
        - db: a database session dependency.
    
    Returns:
        - The product response model for the specified product_id.
    """
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product from the database.

    Parameters:
        product_id (int): The ID of the product to be deleted.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ProductResponse: The deleted product.

    Raises:
        HTTPException: If the product is not found.
    """
    db_product = delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    """
    Update a product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductUpdate): The updated product data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Product: The updated product.
    Raises:
        HTTPException: If the product is not found.
    """
    db_product = update_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product