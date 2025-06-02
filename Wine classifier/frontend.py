#streamlit run frontend.py

import streamlit as st
import requests

st.title("Wine Quality Prediction")

# Input fields (no min/max, bad quality wine values)
fixed_acidity = st.number_input("Fixed Acidity", value=7.4)
volatile_acidity = st.number_input("Volatile Acidity", value=0.70)
citric_acid = st.number_input("Citric Acid", value=0.00)
residual_sugar = st.number_input("Residual Sugar", value=1.9)
chlorides = st.number_input("Chlorides", value=0.076)
free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", value=11.0)
total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", value=34.0)
density = st.number_input("Density", value=0.9978)
pH = st.number_input("pH", value=3.51)
sulphates = st.number_input("Sulphates", value=0.56)
alcohol = st.number_input("Alcohol", value=9.4)


if st.button("Predict Quality"):
    url = "http://127.0.0.1:8000/predict_wine"  
    inputdata = {
        "fixed_acidity": fixed_acidity,
        "volatile_acidity": volatile_acidity,
        "citric_acid": citric_acid,
        "residual_sugar": residual_sugar,
        "chlorides": chlorides,
        "free_sulfur_dioxide": free_sulfur_dioxide,
        "total_sulfur_dioxide": total_sulfur_dioxide,
        "density": density,
        "pH": pH,
        "sulphates": sulphates,
        "alcohol": alcohol
    }

    try:
        response = requests.post(url, json=inputdata)
        response.raise_for_status()
        result = response.json()
        st.success(f"Prediction: {result.get('message', 'No message returned')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
