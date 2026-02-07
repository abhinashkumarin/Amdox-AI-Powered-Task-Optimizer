# stress_monitor.py

class StressMonitor:
    def __init__(self):
        self.history = []

    def update(self, emotion, confidence):
        """
        Tracks emotional stress over time
        Returns True if HR alert should be sent
        """

        # ⬆️ force minimum confidence for stress emotions
        if emotion in ["Stress", "Sad", "Angry", "Fear"]:
            confidence = max(confidence, 0.7)

        self.history.append((emotion, confidence))

        # keep last 10 entries
        if len(self.history) > 10:
            self.history.pop(0)

        stress_score = 0.0

        for emo, conf in self.history:
            if emo in ["Stress", "Sad", "Angry", "Fear"]:
                stress_score += conf

        # 🔍 DEBUG (VERY IMPORTANT)
        print("STRESS HISTORY:", self.history)
        print("STRESS SCORE:", stress_score)

        # 🔴 Threshold
        return stress_score >= 3.5
