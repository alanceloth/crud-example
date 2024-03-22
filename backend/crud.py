from sqlalchemy.orm import Session
from schemas import ProductUpdate, ProductCreate
from models import ProductModel


def get_product(db: Session, product_id: int):
    """
    Retrieves a product from the database based on the given product ID.

    Parameters:
        db (Session): The database session object.
        product_id (int): The ID of the product to retrieve.

    Returns:
        ProductModel: The retrieved product object, or None if no product is found.
    """
    
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_products(db: Session):
    """
    A function that retrieves all products from the database.

    Parameters:
    db (Session): The database session object to query.

    Returns:
    list: A list of all ProductModel objects retrieved from the database.
    """
    
    return db.query(ProductModel).all()


def create_product(db: Session, product: ProductCreate):
    """
    Creates a new product in the database.

    Args:
        db (Session): The database session object.
        product (ProductCreate): The product object to be created.

    Returns:
        ProductModel: The newly created product object.

    Raises:
        None
    """
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    """
    A function that deletes a product from the database.

    Parameters:
    db (Session): The database session.
    product_id (int): The id of the product to be deleted.

    Returns:
    db_product: The deleted product.
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    """
    Updates a product in the database.

    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to update.
        product (ProductUpdate): The updated product information.

    Returns:
        ProductModel or None: The updated product model if successful, None otherwise.
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None:
        return None

    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.price is not None:
        db_product.price = product.price
    if product.categoria is not None:
        db_product.categoria = product.categoria
    if product.email_fornecedor is not None:
        db_product.email_fornecedor = product.email_fornecedor

    db.commit()
    return db_product