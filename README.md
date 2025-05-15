# 🌾 Rice Crop Disease Detection API with Streamlit

This project is a Machine Learning-powered web application that detects diseases in rice leaves using a Convolutional Neural Network (CNN). The model is trained on 8 rice disease classes and provides the disease name, confidence score, and suggested remedies, including home treatments.

## 🔬 Disease Classes

1. Leaf Blast  
2. Leaf Scald  
3. Brown Spot  
4. Bacterial Leaf Blight  
5. Sheath Blight  
6. Narrow Brown Leaf Spot  
7. False Smut  
8. Rice Hispa  

## 💻 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** FastAPI (for API endpoints, optional)  
- **ML Framework:** TensorFlow / Keras  
- **Language:** Python  
- **Deployment:** Localhost / Streamlit Cloud  

---

## 📸 Features

- Upload a rice leaf image
- Detect the disease from the trained model
- View prediction confidence
- Get curated remedies (including home-based solutions)
- Clean, minimal, and responsive UI

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rice-disease-detector.git
cd rice-disease-detector
```
### 2. Install Requirements

```bash
pip install -r requirements.txt
```
### 3. Run the App Locally

```bash
1. uvicorn app.main:app --reload
2. streamlit run .\streamlit_frontend.py
```

