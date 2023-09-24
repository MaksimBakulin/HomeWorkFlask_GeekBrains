from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product, Order, User

app = FastAPI()

engine = create_engine('sqlite:///shop.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class ProductIn(BaseModel):
    name: str
    description: str
    price: float

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float

class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: str
    status: str

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    date: str
    status: str

class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

@app.post("/products", response_model=ProductOut)
def create_product(product: ProductIn):
    session = Session()
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.get("/products", response_model=List[ProductOut])
def read_products():
    session = Session()
    products = session.query(Product).all()
    return products

@app.get("/products/{product_id}", response_model=ProductOut)
def read_product(product_id: int):
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    return product

@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductIn):
    session = Session()
    db_product = session.query(Product).filter(Product.id == product_id).first()
    for field, value in product.dict().items():
        setattr(db_product, field, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    session = Session()
    db_product = session.query(Product).filter(Product.id == product_id).first()
    session.delete(db_product)
    session.commit()

@app.post("/orders", response_model=OrderOut)
def create_order(order: OrderIn):
    session = Session()
    db_order = Order(**order.dict())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@app.get("/orders", response_model=List[OrderOut])
def read_orders():
    session = Session()
    orders = session.query(Order).all()
    return orders

@app.get("/orders/{order_id}", response_model=OrderOut)
def read_order(order_id: int):
    session = Session()
    order = session.query(Order).filter(Order.id == order_id).first()
    return order

@app.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order: OrderIn):
    session = Session()
    db_order = session.query(Order).filter(Order.id == order_id).first()
    for field, value in order.dict().items():
        setattr(db_order, field, value)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    session = Session()
    db_order = session.query(Order).filter(Order.id == order_id).first()
    session.delete(db_order)
    session.commit()

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    session = Session()
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[UserOut])
def read_users():
    session = Session()
    users = session.query(User).all()
    return users

@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    return user

@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserIn):
    session = Session()
    db_user = session.query(User).filter(User.id == user_id).first()
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    session = Session()
    db_user = session.query(User).filter(User.id == user_id).first()
    session.delete(db_user)
    session.commit()

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)