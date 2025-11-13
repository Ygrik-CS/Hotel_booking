from fastapi import FastAPI
from controller import cart_controller, filter_controller

app = FastAPI(title="Hotel-booking")

app.include_router(cart_controller.router)
app.include_router(filter_controller.router)
@app.get("/")
def root():
    return {"message": "Программа работает!"}