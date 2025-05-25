
#uvicorn main:app --reload

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app=FastAPI()


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

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description="name of patient")]
    city: Annotated[Optional[str], Field(default=None,max_length=12, description="city of patient")]
    age: Annotated[Optional[int], Field(default=None, description="age of patient")]
    gender: Annotated[Optional[Literal['male','female','others']], Field(default=None, description="gender of patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="height of patient in mtrs")]
    weight: Annotated[Optional[float], Field(default=None ,gt=0, description="weight of patient in kgs")]

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data  

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)  

@app.get("/")
def hello():
    return{'message':'Patient Management API'}

@app.get('/about')
def about():
    return{'message':'A fully functional API to manage patients records'}

@app.get('/view')
def view():
   data=load_data()
   return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str= Path(..., description='ID of patients in DB', example='P001', max_length=4)):
    data=load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail=f"{patient_id} patient not found!")
    
@app.get('/sort')
def sort_patients(sort_by: str= Query(..., description=' sort on the basis of height,weight or bmi'), order: str= Query('asc', description=' sort in acessending or descending order')):
    
    valid_fields=['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid valid field select from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="select from  asc or desc")
    
    data= load_data()

    sort_order= True if order=='desc' else False
    
    sorted_data= sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    data= load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="patient already exist")
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})


@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"{patient_id} patient not found!")
    
    existing_patient_info=data[patient_id]
    
    updated_patient_info=patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value

    existing_patient_info['id']=patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id]=existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"{patient_id} patient not found!")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})
    


