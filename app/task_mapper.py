def map_task(emotion):
    return {
        "Happy": "Creative / Brainstorming work",
        "Neutral": "Routine operational tasks",
        "Sad": "Low workload + support",
        "Stress": "Break + HR check-in",
        "Angry": "Cool-down tasks",
        "Fear": "Reassurance + guidance",
        "Surprise": "Event review / situational analysis"
    }.get(emotion, "Routine work")
