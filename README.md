# Fake vs Original Review Analyzer

## Project Description

Fake vs Original Review Analyzer is an AI/ML project that uses Natural Language Processing to classify online reviews as potentially Fake or Original.

## Technologies Used

- Python
- Machine Learning
- Natural Language Processing
- TF-IDF
- Logistic Regression
- Streamlit
- Pandas
- Scikit-learn

## Project Workflow

User Review
    ↓
Text Preprocessing
    ↓
TF-IDF Feature Extraction
    ↓
Machine Learning Model
    ↓
Fake / Original Prediction
    ↓
Confidence + Sentiment + Statistics

## Installation

Open Command Prompt inside the project folder.

Install the required libraries:

pip install -r requirements.txt

## Train the Model

Run:

python train_model.py

This creates:

model.pkl
vectorizer.pkl

## Run the Application

Run:

streamlit run app.py

The application will open in your browser.

## Features

- Review classification
- Fake/Original prediction
- AI confidence
- Sentiment detection
- Word count
- Character count
- Sample reviews
- Simple Streamlit interface