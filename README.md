# 🏠 Real Estate Investment Advisor

A modern **Streamlit-based web application** that helps users analyze real estate properties, visualize market trends, and identify profitable investment opportunities.

---

## 📌 Overview

The **Real Estate Investment Advisor** is designed to assist property buyers and investors in making **data-driven decisions**.  
It analyzes property data such as price, size, location, and amenities to provide insights and future value estimation.

---

## 🚀 Features

- 🔐 Secure Login & Signup System (SQLite)
- 🎨 Professional Dark Real Estate Theme UI
- 📊 Executive Dashboard with Key Metrics
- 📈 Interactive Data Visualizations (Plotly)
- 🔎 Property Filtering (Price, City, Type, BHK)
- 🔮 Good Investment Prediction (Rule-Based)
- 💰 Future Property Price Estimation (5 Years)
- 📄 Dataset Preview

---

## 📊 Dashboard Metrics

- Total Properties  
- Average Price  
- Average Size (SqFt)  
- Price per SqFt  
- Good Investment Count  

---

## 📈 Visualizations Included

- Average Price by City & State  
- Property Type Distribution  
- BHK Distribution  
- Furnished Status Analysis  
- Owner Type Analysis  
- Nearby Schools vs Price  
- Nearby Hospitals vs Price  
- Parking Space vs Price  
- Age of Property vs Price  
- Future Price Trends  
- Correlation Heatmap  

---

## 🔮 Investment Prediction Logic

The application identifies **Good Investment** based on:

- Lower Price per SqFt  
- Higher Nearby Schools Count  
- Higher Nearby Hospitals Count  


### 📌 Future Price Calculation:
Future Price = Current Price × 1.35


---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Plotly  
- SQLite  
- Joblib  
- Scikit-learn  
- MLflow  

---

## 📂 Project Structure


Real-Estate-Investment-Advisor/
│
├── app.py
├── train_model.ipynb
├── requirements.txt
├── india_housing_prices.csv
├── users.db
├── models/
│ ├── classification_model.pkl
│ ├── regression_model.pkl
│ ├── scaler.pkl
│ ├── label_encoders.pkl
│ └── feature_columns.pkl
└── README.md
## 🔐 Authentication System

- New users can **create an account**
- Existing users can **log in**
- User data is stored securely in **SQLite database**

---

## 🎯 Project Objective

To build a **real-world analytics application** that helps users:

- Analyze real estate trends  
- Compare property values  
- Identify profitable investments  
- Predict future property prices  

---

## 📌 Outcome

This project demonstrates:

- Data Analysis & Visualization  
- Dashboard Development  
- UI/UX Design  
- Real-world Problem Solving  
