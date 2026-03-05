import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# --- Configuration ---
DATASET_PATH = "brainmridataset" 
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

# --- 1. Data Loading & Preprocessing ---
# Using ImageDataGenerator for loading, resizing, normalizing, and augmenting.
# Splitting dataset into 80% train and 20% validation.
print("Loading and preprocessing data...")

datagen = ImageDataGenerator(
    rescale=1./255,          # Normalize pixel values
    rotation_range=20,       # Augmentation
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    validation_split=0.2     # 20% for validation
)

train_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    classes=['no', 'yes'],
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    classes=['no', 'yes'],
    class_mode='binary',
    subset='validation'
)

# --- 2. Model Architecture ---
print("Building CNN model...")

model = Sequential([
    # Block 1
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
    MaxPooling2D(pool_size=(2, 2)),
    
    # Block 2
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # Block 3
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid') # Binary classification
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# --- 3. Training ---
print("Starting training...")

os.makedirs('model', exist_ok=True)
checkpoint_path = 'model/brain_tumor_model.h5'

callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    ModelCheckpoint(filepath=checkpoint_path, monitor='val_accuracy', save_best_only=True)
]

from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# Compute unbalanced weights directly from the generator
class_weights_array = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_generator.classes),
    y=train_generator.classes
)
# Convert arrays into a dict for Keras
class_weight_dict = dict(enumerate(class_weights_array))

print(f"Applying Class Weights: {class_weight_dict}")

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=callbacks,
    class_weight=class_weight_dict
)

# Force save final model in case checkpoint doesn't trigger on last epoch
model.save(checkpoint_path)
print(f"Model saved to {checkpoint_path}")

# --- 4. Plot Training Curves (Optional) ---
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy over Epochs')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss over Epochs')
plt.legend()

plt.savefig('model/training_history.png')
print("Training history plot saved to model/training_history.png")
