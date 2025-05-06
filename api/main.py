from fastapi import FastAPI
from pydantic import BaseModel
from journal_pipeline import analyze_text, analyze_audio, supabase
from datetime import datetime

app = FastAPI()

# Emotion label mapping
emotion_label_mapping = {
    "LABEL_0": "anger",
    "LABEL_1": "joy",
    "LABEL_2": "fear",
    "LABEL_3": "sadness",
    "LABEL_4": "surprise",
    "LABEL_5": "disgust",
    "LABEL_6": "trust",
    "LABEL_7": "anticipation",
    "LABEL_8": "love",
    "LABEL_9": "optimism",
    "LABEL_10": "pessimism",
    "LABEL_11": "contentment",
    "LABEL_12": "confusion",
    "LABEL_13": "boredom",
    "LABEL_14": "excitement",
    "LABEL_15": "pride",
    "LABEL_16": "guilt",
    "LABEL_17": "fear",
    # Add all labels here as per your model's output
}

# Pydantic model to receive the user ID in POST request
class UserRequest(BaseModel):
    user_id: str

# POST endpoint to trigger emotion analysis
@app.post("/analyze")
def analyze(user: UserRequest):
    print(f"\n🔍 [ANALYSIS REQUEST] Received request for user_id: {user.user_id}")

    # 1. Fetch latest journal entry for this user
    response = supabase.table("journal_entries")\
        .select("*")\
        .eq("user_id", user.user_id)\
        .order("timestamp", desc=True)\
        .limit(1)\
        .execute()

    entries = response.data
    print(f"📄 [FETCH ENTRY] Found journal entries: {entries}")

    if not entries:
        print("⚠️ [NO ENTRY] No journal entries found for this user.")
        return {"error": "No journal entries found for this user."}

    entry = entries[0]
    text_entry = entry.get("text_entry")
    audio_path = entry.get("audio_entry")
    timestamp = entry["timestamp"]

    print(f"📝 [ENTRY DETAILS] Timestamp: {timestamp}, Text: {text_entry}, Audio: {audio_path}")

    # 2. Run analysis
    text_label, text_scores = None, []
    audio_label, audio_scores = None, []

    if text_entry:
        print("🔠 [TEXT ANALYSIS] Starting...")
        text_label, text_scores = analyze_text(text_entry)
        text_label = emotion_label_mapping.get(text_label, "Unknown")  # Map label to emotion
        print(f"✅ [TEXT RESULT] Label: {text_label}, Scores: {text_scores}")

    if audio_path:
        print("🎧 [AUDIO ANALYSIS] Starting...")
        audio_label, audio_scores = analyze_audio(audio_path)
        audio_label = emotion_label_mapping.get(audio_label, "Unknown")  # Map label to emotion
        print(f"✅ [AUDIO RESULT] Label: {audio_label}, Scores: {audio_scores}")

    # 3. Store analysis result in 'ai_analysis' table
    result = supabase.table("ai_analysis").insert({
        "user_id": user.user_id,
        "timestamp": timestamp,
        "text_emotion_label": text_label,
        "text_scores": text_scores,
        "audio_emotion_label": audio_label,
        "audio_scores": audio_scores,
        "day_label": text_label or audio_label,
        "day_score": max(text_scores + audio_scores) if (text_scores or audio_scores) else None
    }).execute()

    print("💾 [SAVE RESULT] Inserted into ai_analysis:", result)

    return {
        "text_label": text_label,
        "audio_label": audio_label,
        "text_scores": text_scores,
        "audio_scores": audio_scores,
        "status": "✅ Analysis completed and saved."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


