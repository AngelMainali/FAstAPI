
# uvicorn sec_main:new_app --reload

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal 



class Patient(BaseModel):
    
    id:Annotated[str, Field(..., description="id of patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="name of patient")]
    city: Annotated[str, Field(...,max_length=12, description="city of patient")]
    age: Annotated[int, Field(..., description="age of patient")]
    gender: Annotated[Literal['male','female','others'], Field(..., description="gender of patient")]
    height: Annotated[float, Field(..., gt=0, description="height of patient in mtrs")]
    weight: Annotated[float, Field(...,gt=0, description="weight of patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi= round((self.weight)/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi< 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'

new_app= FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data,f)

@new_app.get('/')
def hi():
    return{'message':'I am done'}

@new_app.get('/about')
def about():
    return{'message':'I am about patient management system'}

@new_app.get('/view')
def view():
    data=load_data()
    return data 

@new_app.get('/patient/{patient_id}')
def view_patient(patient_id: str=Path(..., title='patient id', description='enter patient id', examples='P001', max_length=10, min_length=4)):
    data= load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@new_app.post('/create')
def create_patient(patient: Patient):
    data= load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail=f"patient with patient no {patient.id} already exist")
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@new_app.get('/sort') #http://localhost:8000/sort?sort_by=height&order=desc
def sort_patient(sort_by: str= Query(..., description="sort by height, weight, bmi "), order: str=Query('asc', description='sort asc or desc')):
    
    valid_fields=['height','weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="inavlid field to sort")
 
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="select either asc or desc")
    
    data=load_data()

    sort_order= True if order=='desc' else False

    sorted_data= sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
