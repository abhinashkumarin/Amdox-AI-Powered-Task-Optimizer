from deepface import DeepFace

class EmotionDetector:
    def __init__(self):
        self.last_emotion = ("Neutral", 0.5)

    def detect(self, frame):
        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )

            emotions = result[0]["emotion"]
            dominant = max(emotions, key=emotions.get)
            confidence = emotions[dominant] / 100

            self.last_emotion = (dominant.capitalize(), round(confidence, 2))
            return self.last_emotion

        except Exception:
            return self.last_emotion
