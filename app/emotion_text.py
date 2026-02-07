# emotion_text.py

from textblob import TextBlob
import re

# ======================================================
# 🌍 EMOTION KEYWORDS
# ======================================================

EMOTION_KEYWORDS = {
    "Happy": ["happy", "excited", "positive"],

    "Sad": ["sad", "depressed", "down", "mentally tired"],

    "Angry": ["angry", "furious", "mad"],

    "Stress": ["stress", "stressed", "pressure", "tired", "overworked"],

    "Fear": ["fear", "scared", "afraid", "worried"],

    # ➕ ADDED (NO EXISTING LOGIC REMOVED)
    "Surprise": [
        "surprise", "surprised", "shocked", "unexpected",
        "omg", "oh my god", "what", "really",
        "arey", "arre"
    ],
}

# ======================================================
# 🧠 TEXT EMOTION DETECTOR
# ======================================================

def detect_text_emotion(text: str):
    if not text or not text.strip():
        return "Neutral", 0.35

    text_clean = text.lower()
    emotion_scores = {emo: 0 for emo in EMOTION_KEYWORDS}

    # -----------------------------
    # 1️⃣ KEYWORD MATCHING (UNCHANGED)
    # -----------------------------
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in text_clean:
                emotion_scores[emotion] += 1

    # -----------------------------
    # 2️⃣ SURPRISE REACTION BOOST (ADDITIVE)
    # -----------------------------
    if re.search(r"(!{1,}|\?{2,}|omg|oh my god|arey|arre)", text_clean):
        emotion_scores["Surprise"] += 2

    # -----------------------------
    # 3️⃣ DOMINANT EMOTION (UNCHANGED)
    # -----------------------------
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    max_score = emotion_scores[dominant_emotion]

    # -----------------------------
    # 4️⃣ SENTIMENT BACKUP (UNCHANGED)
    # -----------------------------
    polarity = TextBlob(text_clean).sentiment.polarity

    if max_score == 0:
        if polarity < -0.3:
            dominant_emotion = "Sad"
            confidence = 0.6
        else:
            return "Neutral", 0.35
    else:
        confidence = min(0.95, 0.4 + max_score * 0.2)

    # -----------------------------
    # 🔴 IMPORTANT FIX (AS REQUESTED)
    # -----------------------------
    if dominant_emotion in ["Stress", "Sad", "Angry", "Fear"]:
        confidence = max(confidence, 0.7)

    # ➕ SURPRISE CONFIDENCE FLOOR (SAFE ADD)
    if dominant_emotion == "Surprise":
        confidence = max(confidence, 0.65)

    return dominant_emotion, round(confidence, 2)
