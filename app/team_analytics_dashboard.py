import streamlit as st
import pandas as pd
import plotly.express as px
import re
from pathlib import Path

st.set_page_config(page_title="Team Mood Dashboard", layout="wide")
st.title("Team Analytics – Mood Dashboard")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "team_mood.csv"

def load_data(path: Path):
    if not path.exists():
        st.error(f"Data file not found: {path}")
        return pd.DataFrame(columns=["emp", "emotion_raw", "time", "emotion", "confidence"])
    df = pd.read_csv(path, header=None, names=["emp", "emotion_raw", "time"])
    def parse_emotion(s):
        if pd.isna(s):
            return ("Neutral", 0.0)
        s = str(s).strip()
        m = re.search(r"['\"]?([A-Za-z]+)['\"]?,?\s*([0-9\.]+)?", s)
        if m:
            label = m.group(1).capitalize()
            conf = float(m.group(2)) if m.group(2) else 0.0
            if conf > 1:  # values in file may be percentages like 99.3
                conf = conf / 100.0
            return (label, conf)
        return (s, 0.0)
    parsed = df["emotion_raw"].apply(lambda s: pd.Series(parse_emotion(s), index=["emotion", "confidence"]))
    df = pd.concat([df, parsed], axis=1)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    return df

df = load_data(DATA_PATH)

st.sidebar.header("Filters")
min_conf = st.sidebar.slider("Min confidence", 0.0, 1.0, 0.0, 0.01)
emotion_filter = st.sidebar.multiselect("Emotions", options=sorted(df["emotion"].dropna().unique()), default=sorted(df["emotion"].dropna().unique()))

filtered = df[(df["confidence"] >= min_conf) & (df["emotion"].isin(emotion_filter))]

st.header("Summary")
counts = filtered.groupby("emotion").size().reset_index(name="count")
if counts.empty:
    st.info("No data available for the selected filters.")
else:
    fig = px.bar(counts, x="emotion", y="count", color="emotion", title="Emotion distribution")
    st.plotly_chart(fig, use_container_width=True)

st.header("Recent Entries")
st.dataframe(filtered.sort_values("time", ascending=False).head(200), use_container_width=True)

st.caption(f"Data file: {DATA_PATH}")

