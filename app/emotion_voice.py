import sounddevice as sd
import numpy as np
import librosa
import tensorflow as tf

MODEL = tf.keras.models.load_model("../Models/voice_emotion_cnn.keras")

EMOTIONS = ["Happy", "Angry", "Fear", "Stress", "Surprise", "Neutral"]

SAMPLE_RATE = 16000
DURATION = 4


def record_audio():
    audio = sd.rec(int(DURATION * SAMPLE_RATE),
                    samplerate=SAMPLE_RATE,
                    channels=1)
    sd.wait()
    return audio.flatten()


def extract_mfcc(audio):
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=SAMPLE_RATE,
        n_mfcc=40
    )
    mfcc = np.mean(mfcc.T, axis=0)
    return mfcc.reshape(1, 40, 1)


def detect_voice_emotion():
    audio = record_audio()

    # 🔇 Silence detection
    energy = np.mean(np.abs(audio))
    if energy < 0.008:
        return "Neutral", 0.40

    features = extract_mfcc(audio)

    probs = MODEL.predict(features, verbose=0)[0]

    # 🧠 Softmax output (model decision)
    idx = int(np.argmax(probs))
    emotion = EMOTIONS[idx]
    confidence = float(probs[idx])

    # 🧠 Uncertainty handling (entropy)
    entropy = -np.sum(probs * np.log(probs + 1e-8))

    if entropy > 1.5:
        confidence *= 0.75  # model unsure

    return emotion, round(confidence, 2)
