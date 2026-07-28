import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ------------------------
# Load Dataset
# ------------------------

df = pd.read_csv("datasets/document_dataset.csv")

texts = df["text"].values
labels = df["category"].values

# ------------------------
# Encode Labels
# ------------------------

encoder = LabelEncoder()

labels = encoder.fit_transform(labels)

# Save label names
label_names = encoder.classes_

# ------------------------
# Train/Test Split
# ------------------------

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42
)

# ------------------------
# Text Vectorization
# ------------------------

vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=5000,
    output_sequence_length=100
)

vectorizer.adapt(X_train)

# ------------------------
# Build Model
# ------------------------

model = tf.keras.Sequential([
    vectorizer,
    tf.keras.layers.Embedding(5000, 64),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(len(label_names), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ------------------------
# Train
# ------------------------

model.fit(
    X_train,
    y_train,
    epochs=15,
    validation_data=(X_test, y_test)
)

# ------------------------
# Evaluate
# ------------------------

loss, accuracy = model.evaluate(X_test, y_test)

print(f"\nAccuracy: {accuracy:.2f}")

# ------------------------
# Save Model
# ------------------------

model.save("models/document_classifier.keras")

print("\nModel saved successfully!")

# ------------------------
# Save Labels
# ------------------------

pd.Series(label_names).to_csv(
    "models/labels.csv",
    index=False,
    header=False
)

print("Labels saved successfully!")