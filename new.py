from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Address(BaseModel):
    city: str
    state:str
    zip : int

address_data={'city':'btm','state':'nep', 'zip':1000}  

address1= Address(**address_data)

class Employee(BaseModel):

    id: Annotated[int, Field(gt=0, lt=100, description="enter emp-if from 0 to 100", example=10, strict=True)]
    email : Annotated[EmailStr, Field(description="enter email")]
    url: Annotated[AnyUrl, Field(description="enter url")]
    position: Annotated[Optional[List[str]], Field(default=None,example=['tester','developer'])]
    name: Annotated[str, Field(description="enter name", max_length=20, min_length=2)]
    salary: Annotated[float, Field(description="enter salary", gt=0, strict=True)]
    address: Address 

    @computed_field
    @property
    def annual_Salary(self) -> float:
        annual= self.salary*12
        return annual
    
    @field_validator('salary')
    @classmethod
    def validate_salary(cls, value):
        if value < 0:
            raise ValueError("Salary must be above 0 ")
        elif value > 1000000:
            raise ValueError("salary system is being mishandled")
        else:
             return value
        

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        domain=['gov.com','np.com']
        domain_name= value.split('@')[-1]
        if domain_name not in domain:
            raise ValueError("invalid domain")
        return value   
    
    
    @model_validator(mode='after')
    def validate_position(cls, model):
        if model.position is not None:
            for position in model.position:
                if position not in ['tester', 'developer']:
                    raise ValueError("position must be tester or developer")
        return model

employee_data={'id':10, 'email':'you@gov.com', 'url':'https://www.google.com', 'position':['developer'], 'name':'angel', 'salary': 20, 'address':address1}

employee1=Employee(**employee_data)

print(employee1)

