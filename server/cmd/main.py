from fastapi import FastAPI
from routes import cart_routes

app = FastAPI(title="Hotel-booking")

app.include_router(cart_routes)
#app.include_router(filter_controller.router)
@app.get("/")
def root():
    return {"message": "Программа работает!"}