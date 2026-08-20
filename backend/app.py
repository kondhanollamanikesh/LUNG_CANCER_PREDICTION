from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import pandas as pd


app = FastAPI()


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load trained Random Forest model
with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)


# Data received from React
class PatientData(BaseModel):

    YELLOW_FINGERS: int
    ANXIETY: int
    PEER_PRESSURE: int

    CHRONIC_DISEASE: int = Field(
        alias="CHRONIC DISEASE"
    )

    FATIGUE: int
    ALLERGY: int
    WHEEZING: int

    ALCOHOL_CONSUMING: int = Field(
        alias="ALCOHOL CONSUMING"
    )

    COUGHING: int

    SWALLOWING_DIFFICULTY: int = Field(
        alias="SWALLOWING DIFFICULTY"
    )

    CHEST_PAIN: int = Field(
        alias="CHEST PAIN"
    )

    class Config:
        populate_by_name = True


@app.get("/")
def home():

    return {
        "message": "ML Prediction API is running"
    }


@app.post("/predict")
def predict(data: PatientData):

    # Create derived feature
    ANXYELFIN = (
        data.ANXIETY *
        data.YELLOW_FINGERS
    )


    # Create DataFrame with EXACT model feature names
    input_data = pd.DataFrame([{

        "YELLOW_FINGERS":
            data.YELLOW_FINGERS,

        "ANXIETY":
            data.ANXIETY,

        "PEER_PRESSURE":
            data.PEER_PRESSURE,

        "CHRONIC DISEASE":
            data.CHRONIC_DISEASE,

        "FATIGUE":
            data.FATIGUE,

        "ALLERGY":
            data.ALLERGY,

        "WHEEZING":
            data.WHEEZING,

        "ALCOHOL CONSUMING":
            data.ALCOHOL_CONSUMING,

        "COUGHING":
            data.COUGHING,

        "SWALLOWING DIFFICULTY":
            data.SWALLOWING_DIFFICULTY,

        "CHEST PAIN":
            data.CHEST_PAIN,

        "ANXYELFIN":
            ANXYELFIN

    }])


    # Debugging
    print("\nInput received:")
    print(input_data)

    print("\nInput shape:")
    print(input_data.shape)


    # Prediction
    prediction = model.predict(input_data)


    if prediction[0] == 1:
        result = "Lung Cancer Detected"
    else:
        result = "No Lung Cancer Detected"

    return {
        "prediction": result
    }