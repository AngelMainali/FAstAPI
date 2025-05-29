from fastapi.responses import JSONResponse
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import pickle
import pandas as pd

with open(r'trained_model.sav', 'rb') as f:
    model = pickle.load(f)


app=FastAPI() 
#uvicorn app:app --reload


class UserInput(BaseModel):
    fixed_acidity:Annotated[float, Field(...,gt=0,)]
    volatile_acidity:Annotated[float, Field(...,)]
    citric_acid:Annotated[float, Field(...,)]
    residual_sugar:Annotated[float, Field(...,)]
    chlorides:Annotated[float, Field(...,)]
    free_sulfur_dioxide:Annotated[float, Field(...,)]
    total_sulfur_dioxide:Annotated[float, Field(...,)]
    density:Annotated[float, Field(...,)]
    pH:Annotated[float, Field(...,gt=-1,lt=8)]
    sulphates:Annotated[float, Field(...,)]
    alcohol:Annotated[float, Field(...,)]

from fastapi import HTTPException

@app.post('/predict')
def predict(data: UserInput):
    try:
        input_df = pd.DataFrame([{
            'fixed acidity': data.fixed_acidity,
            'volatile acidity': data.volatile_acidity,
            'citric acid': data.citric_acid,
            'residual sugar': data.residual_sugar,
            'chlorides': data.chlorides,
            'free sulfur dioxide': data.free_sulfur_dioxide,
            'total sulfur dioxide': data.total_sulfur_dioxide,
            'density': data.density,
            'pH': data.pH,
            'sulphates': data.sulphates,
            'alcohol': data.alcohol
        }])
        
        prediction = model.predict(input_df)[0]
        prediction = int(prediction)  # Convert from NumPy int64 to native int

        # Determine quality
        quality_message = "Good Quality Wine" if prediction == 1 else "Bad Quality Wine"

        return JSONResponse(status_code=200, content={
            'prediction': prediction,
            'message': quality_message
        })
    
    except Exception as e:
        print("Prediction error:", e)
        raise HTTPException(status_code=500, detail=str(e))