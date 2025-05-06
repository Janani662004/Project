import datetime
from supabase import create_client, Client

# === Supabase Credentials ===
SUPABASE_URL = "https://cfdtkaiekghgymciyqxd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNmZHRrYWlla2doZ3ltY2l5cXhkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MzY5NzE1MSwiZXhwIjoyMDU5MjczMTUxfQ.-XBNHaPzvLgfU8jneukdfdoHG-GUjBi514vSD5c8jzI"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Step 1: Insert Dummy User ===
dummy_user = {
    "id": "3fa85f64-5717-4562-b4fc-2c963f66afa6",
    "username": "jan_dummy",
    "email": "jan66@dummy.com",
    "institution": "Dummy Institute",
    "password": "1234"
}
user_response = supabase.table("users").insert(dummy_user).execute()
print("✅ Dummy user inserted:")
print(user_response)

# === Step 2: Insert Journal Entry ===
dummy_entry = {
    "user_id": dummy_user["id"],
    "text_entry": "I feel really low and unmotivated today.",
    "audio_entry": None,
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
}
journal_response = supabase.table("journal_entries").insert(dummy_entry).execute()
print("📝 Journal Entry Inserted:")
print(journal_response)

# === Step 3: Insert AI Analysis ===
dummy_analysis = {
    "user_id": dummy_user["id"],
    "day_score": 0.73,
    "day_label": "hopeful",
    "weekly_score": 0.62,
    "weekly_label": "neutral",
    "recommended_activities": "Take a short break, go for a walk",
    "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
}
analysis_response = supabase.table("ai_analysis").insert(dummy_analysis).execute()
print("📊 AI Analysis Inserted:")
print(analysis_response)
