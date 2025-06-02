# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 16:21:08 2025

@author: Dell
"""
import pandas as pd
import numpy as np
import pickle
import streamlit as st

movies = pd.read_csv('C:/Users/Dell/Desktop/machine_leraning/Deployed Model/MovieRecommendationEngine/movies.csv')

#loading saved model
knn=pickle.load(open('C:/Users/Dell/Desktop/machine_leraning/Deployed Model/MovieRecommendationEngine/trained_model .sav','rb'))
final_dataset=pickle.load(open('C:/Users/Dell/Desktop/machine_leraning/Deployed Model/MovieRecommendationEngine/final_dataset.sav','rb'))
csr_dataset=pickle.load(open('C:/Users/Dell/Desktop/machine_leraning/Deployed Model/MovieRecommendationEngine/csr_dataset.sav','rb'))

def get_movie_recommendation(movie_name,n_movies_to_recommend = 5):

    movie_list = movies[movies['title'].str.contains(movie_name)]
    if len(movie_list):
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = knn.kneighbors(csr_dataset[movie_idx],n_neighbors=n_movies_to_recommend+1)
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[1:]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_recommend+1))
        return df
    else:
        return "No movies found. Please check your input"
    

def main():

    # Streamlit UI
    st.title("Movie Recommendation System")
    st.write("Enter a movie name to get recommendations:")
    
    # Create an input field for the movie name
    movie_name = st.text_input("Movie Name:")
    
    # Show recommendations when a movie is input
    if movie_name:
        recommendations = get_movie_recommendation(movie_name, n_movies_to_recommend=5)
        
        if isinstance(recommendations, pd.DataFrame):
            st.write("### Recommended Movies:")
            st.dataframe(recommendations)
        else:
            st.write(recommendations)
   
if __name__=='__main__':
    main()        