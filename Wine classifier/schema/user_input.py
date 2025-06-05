from fastapi.responses import JSONResponse
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional



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
