# cd "C:\Users\Dell\Desktop\fast api\Movie Recommendation system"
#streamlit run frontend.py

import streamlit as st
import requests

# Title
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommendation Engine")

# Description
st.markdown("Enter a movie name below, and get recommendations based on what other users liked! 🚀")

# Input box
movie_name = st.text_input("🔍 Enter a movie title", value="The Matrix")

# Button
if st.button("Get Recommendations"):
    if movie_name.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/recommend_movie",  # Replace with your actual API URL
                    json={"movie_name": movie_name}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Recommendations for: **{data['input_movie']}**")
                    recs = data['recommendations']
                    st.table(recs)
                elif response.status_code == 404:
                    st.error("❌ Movie not found. Please try a different name.")
                else:
                    st.error(f"⚠️ Error: {response.status_code} - {response.json().get('detail')}")
            except Exception as e:
                st.exception(f"🔧 Could not connect to API: {e}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit + FastAPI")
