def fuse_emotions(face, text, voice):
    sources = [face, text, voice]
    sources = [s for s in sources if s]

    emotions = {}
    for emo, conf in sources:
        emotions[emo] = emotions.get(emo, 0) + conf

    final_emotion = max(emotions, key=emotions.get)
    confidence = round(emotions[final_emotion] / len(sources), 2)

    return final_emotion, confidence
