from pydantic import BaseModel

class Address(BaseModel):
     city: str
     state: str
     pin: str
     

class Patient(BaseModel):

     name:str
     age: int
     gender: str
     address: Address  #nested model
    

address_dictionary={'city':'ghailadubba','state':'jhapa','pin':'1212'}    
address1= Address(**address_dictionary)

patient_dictionary={'name':'angel','age':25, 'gender':'male', 'address':address1}
patient1= Patient(**patient_dictionary)


#temp=patient1.model_dump(include=['name','gender'])   #temp=patient1.model_dump_json()
#temp=patient1.model_dump(exclude=['name','gender'])
temp=patient1.model_dump(exclude={'address': ['state']})
print(temp)
print(type(temp))


print(patient1)