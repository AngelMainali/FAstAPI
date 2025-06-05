from pydantic import BaseModel, Field
from typing import Annotated, Dict, Union

class PredictionResponse(BaseModel):
    prediction: Annotated[int, Field(..., ge=0, description="Predicted class label (e.g., 0 or 1)")]
    message: Annotated[str, Field(..., description="Interpretation of prediction (e.g., Good Quality Wine)")]
    confidence: Annotated[float, Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")]
    class_probabilities: Annotated[
        Dict[Union[int, str], float],
        Field(..., description="Probabilities for each class label")
    ]
