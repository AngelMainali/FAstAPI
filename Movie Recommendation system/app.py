from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import pandas as pd
import pickle

app2 = FastAPI()
#uvicorn app:app2 --reload

# Load the movies DataFrame
movies = pd.read_csv(r'C:\Users\Dell\Desktop\fast api\Movie Recommendation system\movies.csv')

# Load csr_dataset
with open(r'C:\Users\Dell\Desktop\fast api\Movie Recommendation system\csr_dataset.sav', 'rb') as f:
    csr_dataset = pickle.load(f)

# Load trained KNN model
with open(r'C:\Users\Dell\Desktop\fast api\Movie Recommendation system\trained_model .sav', 'rb') as f:
    knn = pickle.load(f)

# Load final_dataset (this is likely a DataFrame)
with open(r'C:\Users\Dell\Desktop\fast api\Movie Recommendation system\final_dataset.sav', 'rb') as f:
    final_dataset = pickle.load(f)


# Input model for request
class MovieRequest(BaseModel):
    movie_name: str = Field(..., example="The Matrix", min_length=1)

# Recommendation endpoint
@app2.post("/recommend_movie")
def recommend_movie(data: MovieRequest):
    movie_name = data.movie_name

    # Find movies matching the input string (case insensitive)
    movie_list = movies[movies['title'].str.contains(movie_name, case=False, na=False)]

    if len(movie_list) == 0:
        raise HTTPException(status_code=404, detail="No matching movie found. Please check your input.")

    try:
        # Get the movieId of the first matched movie
        movie_id = movie_list.iloc[0]['movieId']

        # Find the index of this movie in the final_dataset
        movie_idx = final_dataset[final_dataset['movieId'] == movie_id].index[0]

        # Find nearest neighbors using the loaded model
        distances, indices = knn.kneighbors(csr_dataset[movie_idx], n_neighbors=6)

        recommendations = []
        for val in sorted(zip(indices.squeeze().tolist(), distances.squeeze().tolist()), key=lambda x: x[1])[1:]:
            rec_movie_id = final_dataset.iloc[val[0]]['movieId']
            rec_title = movies[movies['movieId'] == rec_movie_id]['title'].values[0]
            recommendations.append({
                "title": rec_title,
                "distance": round(val[1], 4)
            })

        return JSONResponse(status_code=200, content={
            "input_movie": movie_list.iloc[0]['title'],
            "recommendations": recommendations
        })

    except Exception as e:
        print("Recommendation error:", e)
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
