from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    #name: str = Field(min_length=3, max_length=20)
    name: Annotated[str, Field(min_length=3, max_length=20, title='Name of patient', description='character less than 21', examples=['angel','ram'])]
    email: EmailStr 
    linkedin_url: AnyUrl
    age: int  = Field(gt=0, lt=100)
    weight: Annotated[float, Field(gt=0, lt=200, strict=True)]
    #married: bool =False   #default value
    married: Annotated[bool, Field(default=None, description='married or not')]
    allergies: Optional[List[str]]= None  #optional default value
    contact_details: Dict[str, str] = Field(max_length=3)
    height: Annotated[float, Field(gt=0, lt=10, strict=True)]


    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains=['edu.com', 'gov.com']
        domain_name= value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('invalid domain')
        return value

     
    @field_validator('name', mode='after')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        raise ValueError('invalid age . age be between 0 and 100')
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("age above 60 must have emergency contact")
        return model
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi= round(self.weight /(self.height**2),2)
        return bmi


patient_info={ 'name':'angel','email':'anjelmainali@gov.com','linkedin_url':'https://www.linkedin.com/in/john-doe-123456789/','age':'61', 'weight':75.2, 'married':True,'allergies': ['pollen','dust'],  'contact_details':{'email':'abc@gmail.com','phone':'234566', 'emergency':'234543'}, 'height':5.9}

patient1 = Patient(**patient_info)  #validation is ddone here

def insert_patient_info(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.bmi)
    print("inserted")


insert_patient_info(patient1)