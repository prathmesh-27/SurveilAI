import cv2
import tensorflow as tf
import numpy as np

# Function to build the feature extractor using InceptionV3
def build_feature_extractor(input_shape=(224, 224, 3)):
    feature_extractor = tf.keras.applications.InceptionV3(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape,
    )
    feature_extractor.trainable = False
    preprocess_input = tf.keras.applications.inception_v3.preprocess_input

    inputs = tf.keras.Input(input_shape)
    preprocessed = preprocess_input(inputs)
    base_outputs = feature_extractor(preprocessed)
    pooled_outputs = tf.keras.layers.GlobalAveragePooling2D()(base_outputs)
    dense_output = tf.keras.layers.Dense(1024, activation='relu')(pooled_outputs)
    dropout_output = tf.keras.layers.Dropout(0.5)(dense_output)
    final_output = tf.keras.layers.Dense(2048, activation='relu')(dropout_output)
    
    return tf.keras.Model(inputs, final_output, name="feature_extractor")

# Function to load your trained model
def load_model(model_path='app\models\model\classifier.h5'):
    return tf.keras.models.load_model(model_path)

# Initialize the feature extractor and model
feature_extractor = build_feature_extractor()
model = load_model()

# Process a frame for prediction
def process_frame_for_prediction(frame, resize=(224, 224)):
    resized_frame = cv2.resize(frame, resize)
    resized_frame = tf.keras.applications.inception_v3.preprocess_input(resized_frame) 
    # print("frame Processed")
    return resized_frame

# Make prediction on the frame
def make_prediction(processed_frames):
    encodings = feature_extractor.predict(np.array(processed_frames)).astype(np.float32)
    encodings = np.expand_dims(encodings, axis=0) # Add batch dimension
    prediction = model.predict(encodings)
    predicted_class_index = np.argmax(prediction)
    class_labels = ['Abuse', 'Assault', 'Fighting', 'Normal', 'Shoplifting', 'Vandalism']  # Adjust according to your class labels
    last_predicted_class = class_labels[predicted_class_index]
    return last_predicted_class
