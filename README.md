Marketing Analytics Predictor & Optimiser - README

# 1. Project Description
This is a web application designed to predict the total revenue of a marketing campaign based on user-provided parameters. It utilizes a trained XGBoost machine learning model for the core prediction and integrates with the Google Gemini API to generate actionable, data-driven optimization suggestions. The user interface is built with Streamlit.

# 2. Key Technologies

Language: Python
Framework: Streamlit

Machine Learning & Data Processing:

Pandas & NumPy: For data manipulation and numerical operations.
Seaborn & Matplotlib : For data visualization
Scikit-learn: For data pre-processing pipelines modelling
XGBoost: Best fit ML model for prediction
Joblib: For model and pipeline serialization.

API Integration:

Google Generative AI (Gemini): For generating strategic insights.
Requests: For handling HTTP requests.

# 3. How to Run the Project
Follow these steps to set up and run the application on your local machine.

## 3.1. Prerequisites
Python3 or a later version installed.
pip (Python package installer).

## 3.2. Setup Instructions
a. Clone the Repository
Open your terminal and clone the project repository.

Replace with your actual repository URL
git clone [https://github.com/your-username/your-repository.git](https://github.com/your-username/your-repository.git)
cd your-repository

b. Create a Virtual Environment 
It is best practice to create a virtual environment to manage project-specific dependencies.

For Windows
python -m venv venv
.\venv\Scripts\activate

c. Install Dependencies
Install all the required Python packages using the requirements.txt file.
pip install -r requirements.txt

## 3.3. Running the Application
With the setup complete, run the following command in your terminal to start the Streamlit application:
streamlit run main.py

This will start the local server, and the application should open automatically in your default web browser.

# 4. Project File Overview

main.py: Contains the Streamlit user interface code and logic for interacting with the backend and the Gemini API.
backend.py: Includes the functions for data preprocessing, revenue prediction using the loaded model, and generating the Excel download file.
roi_pipeline.joblib: A serialized file containing the complete scikit-learn pipeline, which includes the data scaler and the trained XGBoost model.
requirements.txt: A list of all Python packages required to run the project.
