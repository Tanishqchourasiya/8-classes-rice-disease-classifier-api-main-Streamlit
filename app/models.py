import tensorflow as tf
from .config import config

MODEL_PATH = config["model"]["path"]
IMAGE_SIZE = config["model"]["image_size"]

# Load the model
loaded_model = tf.saved_model.load(MODEL_PATH)

# Get the concrete function for prediction
model = loaded_model.signatures["serving_default"]

# Get class names from config
CLASS_NAMES = config["classes"]
