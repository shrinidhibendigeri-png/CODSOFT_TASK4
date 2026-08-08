# 🎬 Movie Recommendation System

## CODSOFT Internship - Task 4

A simple movie recommendation system built using Python and content-based filtering.

## 📌 Project Overview

This project recommends movies to users based on their movie preferences.

The system analyzes movie information such as:

- Genres
- Keywords
- Cast

It then recommends movies that are most similar to the movie selected by the user.

## 🧠 Recommendation Technique

This project uses **Content-Based Filtering**.

The recommendation process works as follows:

1. Movie information is combined into a single text feature.
2. TF-IDF Vectorization converts the text into numerical vectors.
3. Cosine Similarity calculates the similarity between movies.
4. Movies with the highest similarity scores are recommended to the user.
5. User-selected genres provide an additional preference boost.

## ⚙️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Streamlit
- TF-IDF
- Cosine Similarity

## ✨ Features

- Select a movie you like
- Select favourite genres
- Choose the number of recommendations
- Get personalized movie recommendations
- View movie genres and cast
- View similarity scores
- Interactive web interface using Streamlit

## 📂 Project Structure

```text
CODSOFT_TASK4/
│
├── app.py
├── movies.csv
├── requirements.txt
├── README.md
└── .gitignore