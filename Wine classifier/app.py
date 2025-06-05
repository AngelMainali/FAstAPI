from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
import pandas as pd
from schema.user_input import UserInput
from model.predict import predict_output,model,MODEL_VERSION
from schema.prediction_response import PredictionResponse

app=FastAPI() 
#uvicorn app:app --reload

from fastapi import HTTPException

@app.get('/')
def home():
    return {"message": "Welcome to the Wine Classifier API"}

@app.get('/health')
def health_check():
    return {
        "status": "OK", 
        "version": MODEL_VERSION,
        "model_loaded": model is not None,
        }

@app.post('/predict_wine',response_model=PredictionResponse)
def predict(data: UserInput):
    try:
        user_input = pd.DataFrame([{
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
        
        result = predict_output(user_input)
        prediction = int(result['predicted_category'])
        quality_message = "Good Quality Wine" if prediction == 1 else "Bad Quality Wine"

        return JSONResponse(status_code=200, content={
            'prediction': prediction,
            'message': quality_message,
            'confidence': round(result['confidence'], 4),
            'class_probabilities': result['class_probabilites']
        })
    
    except Exception as e:
        print("Prediction error:", e)
        raise HTTPException(status_code=500, detail=str(e))