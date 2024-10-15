from fastapi import FastAPI
from auth_routes import auth_router
from orders_routes import order_router

app=FastAPI()

app.include_router(auth_router)
app.include_router(order_router)

@app.get("/")
def root():
    return{"message":"Hello World"}