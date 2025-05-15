import numpy as np
import tensorflow as tf
from .models import model, IMAGE_SIZE, CLASS_NAMES

def predict_image(image):
    img = tf.keras.preprocessing.image.load_img(image, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    # Get the input tensor name
    input_tensor_name = list(model.structured_input_signature[1].keys())[0]

    # Make prediction
    predictions = model(**{input_tensor_name: img_array})

    # Get the output tensor name
    output_tensor_name = list(predictions.keys())[0]

    # Get the prediction values
    prediction_values = predictions[output_tensor_name].numpy()

    predicted_class = CLASS_NAMES[np.argmax(prediction_values[0])]
    confidence = float(round(100 * np.max(prediction_values[0]), 2))

    return predicted_class, confidence
