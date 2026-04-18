import re
import numpy as np
import pandas as pd
import scipy.sparse as sp
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

# Load models saved from the notebook (tfidf, scaler, log_reg)
tfidf = joblib.load("model/tfidf.pkl")
scaler = joblib.load("model/scaler.pkl")
log_reg = joblib.load("model/log_reg.pkl")


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z\s,.'\-\*\+\n!?0-9]", "", text)
    return text


def get_burstiness(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0
    sentences = re.split(r"[.!?]+", text)
    lengths = [len(s.split()) for s in sentences if len(s.strip()) > 0]
    return np.std(lengths) if len(lengths) > 0 else 0


def get_comma_density(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0
    words = len(text.split())
    if words == 0:
        return 0
    return (text.count(",") / words) * 100


def get_personal_pronoun_density(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0
    words = re.findall(r"\b[a-z]+\b", text)
    if len(words) == 0:
        return 0
    pronouns = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ourselves"}
    count = sum(1 for w in words if w in pronouns)
    return (count / len(words)) * 100


def get_contraction_density(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0
    words = len(re.findall(r"\b[a-z]+\b", text))
    if words == 0:
        return 0
    contractions = len(re.findall(r"[a-z]+'[a-z]+", text))
    return (contractions / words) * 100


def get_repeated_phrase_density(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0
    words = re.findall(r"\b[a-z]+\b", text)
    if len(words) < 3:
        return 0
    trigrams = [" ".join(words[i:i+3]) for i in range(len(words) - 2)]
    if len(trigrams) == 0:
        return 0
    from collections import Counter
    counts = Counter(trigrams)
    repeated = sum(c - 1 for c in counts.values() if c > 1)
    return (repeated / len(trigrams)) * 100


def predict(text):
    cleaned = clean_text(text)

    # 5 stylometric features in the same order as in the notebook
    stats = pd.DataFrame([[
        get_burstiness(cleaned),
        get_comma_density(cleaned),
        get_personal_pronoun_density(cleaned),
        get_contraction_density(cleaned),
        get_repeated_phrase_density(cleaned),
    ]], columns=[
        "burstiness", "comma_density", "pronoun_density",
        "contraction_density", "repeated_phrase_density",
    ])

    # Scale stats with the same scaler used during training
    stats_scaled = scaler.transform(stats)
    stats_scaled_sparse = sp.csr_matrix(stats_scaled)

    # TF-IDF features
    tfidf_text = tfidf.transform([cleaned])

    # Fuse TF-IDF and scaled stats
    final_input = sp.hstack([tfidf_text, stats_scaled_sparse])

    # Predict
    prediction = log_reg.predict(final_input)[0]
    probabilities = log_reg.predict_proba(final_input)[0]

    return {
        "label": "AI Generated" if prediction == 1 else "Human Written",
        "is_ai": bool(prediction == 1),
        "ai_pct": round(float(probabilities[1]) * 100, 2),
        "human_pct": round(float(probabilities[0]) * 100, 2),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("text", "").strip()
        if input_text:
            result = predict(input_text)

    return render_template("index.html", result=result, input_text=input_text)


if __name__ == "__main__":
    app.run()