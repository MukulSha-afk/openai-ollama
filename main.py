from fastapi import FastAPI
from pydantic import BaseModel
from ml_model import predict_food

app = FastAPI()

class UserInput(BaseModel):
    age: int
    height: int
    weight: int
    goal: str
    meal_time: str

@app.post("/predict")
def predict(user: UserInput):
    result = predict_food(
        user.age,
        user.height,
        user.weight,
        user.goal,
        user.meal_time
    )
    return result