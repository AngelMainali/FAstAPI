import pickle
import pandas as pd

with open(r'model/trained_model.sav', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION= '1.0.0'  #demo version  

class_labels= model.classes_.tolist()
print(class_labels)

def predict_output(user_input: dict):
    input_df = pd.DataFrame(user_input)
    predicted_class= model.predict(input_df)[0]
  
    probabilities= model.predict_proba(input_df)[0]
    confidence= max(probabilities)

    class_probs= dict(zip(class_labels, map(lambda p: round(p,4),probabilities)))
    
    return{
         'predicted_category':predicted_class,
         'confidence':confidence,
         'class_probabilites':class_probs,
    }

    
