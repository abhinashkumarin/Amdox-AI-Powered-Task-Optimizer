import os
import librosa
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

DATASET_PATH = "datasets"
EMOTIONS = ["happy", "angry", "fear", "stress", "surprise", "neutral"]
SAMPLE_RATE = 16000
MFCCS = 40

X, y = [], []

def extract_mfcc(path):
    audio, sr = librosa.load(path, sr=SAMPLE_RATE)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=MFCCS)
    return np.mean(mfcc.T, axis=0)

# ---------------- LOAD DATA ----------------
for idx, emotion in enumerate(EMOTIONS):
    folder = os.path.join(DATASET_PATH, emotion)

    if not os.path.exists(folder):
        print(f"⚠ Folder missing: {folder}")
        continue

    for file in os.listdir(folder):
        if file.endswith(".wav"):
            try:
                features = extract_mfcc(os.path.join(folder, file))
                X.append(features)
                y.append(idx)
            except Exception as e:
                print(f"❌ Error {file}: {e}")

# ---------------- CHECK DATA ----------------
if len(X) == 0:
    raise RuntimeError(
        "❌ No audio samples found!\n"
        "👉 Add .wav files inside Models/datasets/<emotion>/"
    )

X = np.array(X)
y = tf.keras.utils.to_categorical(y, num_classes=len(EMOTIONS))

print(f"✅ Samples loaded: {X.shape[0]}")

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL ----------------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(MFCCS,)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(len(EMOTIONS), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ---------------- TRAIN ----------------
model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=30,
    batch_size=16
)

# ---------------- SAVE ----------------
model.save("voice_emotion_cnn.keras")
print("🎉 Model trained & saved: voice_emotion_cnn.keras")
