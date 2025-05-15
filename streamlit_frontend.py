import streamlit as st
from PIL import Image
import requests
import io
import json


FASTAPI_URL = "http://localhost:8000/predict"
PAGE_TITLE = "PlantMD: AI Crop Doctor"
PAGE_ICON = "🌿"


def preprocess_image(image_pil):
    img_byte_arr = io.BytesIO()
    if image_pil.mode == 'RGBA':
        image_pil = image_pil.convert('RGB')
    image_pil.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def make_api_request(image_bytes, filename="image.jpg"):
    files = {"file": (filename, image_bytes, "image/jpeg")}
    try:
        response = requests.post(FASTAPI_URL, files=files, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "ConnectionError", "message": "Could not connect to the API. Is the backend server running?"}
    except requests.exceptions.Timeout:
        return {"error": "Timeout", "message": "The request to the API timed out."}
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = e.response.json()
            return {"error": "HTTPError", "message": f"API Error (Status {e.response.status_code}): {error_detail.get('detail', e.response.text)}"}
        except json.JSONDecodeError:
            return {"error": "HTTPError", "message": f"API Error (Status {e.response.status_code}): {e.response.text}"}
    except Exception as e:
        return {"error": "Exception", "message": f"An unexpected error occurred: {str(e)}"}


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #F0F2F6;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px 24px;
    border: none;
}
.stButton>button:hover {
    background-color: #45a049;
}
.stFileUploader label {
    font-size: 1.1rem;
    font-weight: bold;
}
.prediction-box {
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
.prediction-header {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2E7D32;
    margin-bottom: 10px;
}

/* New/Modified Confidence Bar Styles */
.confidence-container {
    display: flex;
    align-items: center;
    width: 100%; /* Ensure it takes full available width */
    margin-bottom: 10px; /* Add some space below the bar */
}
.confidence-text-label {
    min-width: 65px; /* Ensures space for "100.00%" */
    font-weight: bold;
    color: #333;
    margin-right: 10px; /* Space between text and bar */
}
.confidence-bar-background {
    flex-grow: 1; /* Allows the bar to take remaining space */
    height: 22px;
    background-color: #e0e0e0; /* Light grey track for the bar */
    border-radius: 5px;
    overflow: hidden; /* Ensures fill doesn't exceed rounded corners */
    position: relative; /* For potential future overlays if needed */
}
.confidence-bar-fill {
    height: 100%;
    border-radius: 5px; /* Match parent's border radius */
    transition: width 0.5s ease-in-out; /* Smooth transition for width change */
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6046/6046120.png", width=100)
    st.markdown(f"<h1 style='text-align: center;'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        **Welcome to PlantMD!** 🩺🌿
        Upload an image of a Crop leaf, and our AI will try to detect
        potential diseases and suggest remedies.
        **How to Use:**
        1.  Click on **"Browse files"** or drag & drop an image.
        2.  Supported formats: JPG, JPEG, PNG.
        3.  Our AI will analyze it and show you the results!
        """
    )
    st.markdown("---")
    st.info("Disclaimer: This AI model is by students of GIT, Jaipur for Major Project **NOT FOR INDUSTRY USAGE")
    st.markdown("---")
    st.markdown("Made with 💚 by Tanishq")


st.title(f"🍃 {PAGE_TITLE}")
st.markdown("Upload a leaf image, and let our AI diagnose its health!")

uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your Uploaded Leaf", use_container_width=True)
        except Exception as e:
            st.error(f"Error opening image: {e}")
            st.stop()

    with col2:
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        st.markdown("<p class='prediction-header'>🔍 Analysis Results:</p>", unsafe_allow_html=True)

        with st.spinner("Our AI is examining your leaf... 🌱"):
            img_bytes = preprocess_image(image)
            prediction_result = make_api_request(img_bytes, uploaded_file.name)

        if "error" in prediction_result:
            st.error(f"**API Error:** {prediction_result['message']}")
        elif prediction_result:
            class_name = prediction_result.get("predicted_class", "N/A")
            confidence_percent = prediction_result.get("confidence", 0.0)
            remedy = prediction_result.get("remedy", "")

            st.markdown(f"**Predicted Condition:**")
            st.markdown(f"<h3 style='color: #1E88E5;'>{class_name.replace('___', ' ').replace('_', ' ')}</h3>", unsafe_allow_html=True)

            st.markdown(f"**Confidence Score:**")
            bar_color = "#4CAF50"
            if confidence_percent < 70: bar_color = "#FFC107"
            if confidence_percent < 40: bar_color = "#F44336"


            st.markdown(f"""
            <div class="confidence-container">
                <div class="confidence-text-label">{confidence_percent:.2f}%</div>
                <div class="confidence-bar-background">
                    <div class="confidence-bar-fill" style="width: {confidence_percent}%; background-color: {bar_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if "healthy" in class_name.lower():
                st.success("🎉 Great news! Your Crop appears to be healthy. Keep up the good care!")
                st.balloons()
            elif class_name != "N/A":
                st.warning("⚠️ Your Crop might have an issue. Please see the details below.")
                if remedy:
                    st.markdown(f"**💡 Suggested Remedy / Management:**")
                    st.info(f"{remedy}")
                else:
                    st.markdown(f"**💡 Suggested Remedy / Management:**")
                    st.caption("No specific remedy information provided by the API for this condition.")
                st.markdown("---")

                st.info(f"Tip: You can also search online for '{class_name.replace('___', ' ').replace('_', ' ')} symptoms and treatment' for more information. 🔍")
            else:
                st.info("Could not determine the condition. Please try a clearer image or a different leaf.")
        else:
            st.error("No prediction received from the API. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("☝️ Upload an image to get started!")
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <img src="https://cdn-icons-png.flaticon.com/512/6046/6046120.png" width="200" alt="A placeholder image of a Crop waiting for analysis">
            <p style="font-size: 1.2rem; color: #555;">Your Crop's health check is just an upload away!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("<p style='text-align:center;'>© 2025 PlantMD - Your AI Crop Health Assistant</p>", unsafe_allow_html=True)