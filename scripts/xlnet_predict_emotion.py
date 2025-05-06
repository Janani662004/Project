import torch
from transformers import XLNetTokenizer, XLNetForSequenceClassification
import torch.nn.functional as F

# Load model and tokenizer
model_path = 'D:/ja/Models/reduced_xlnet'
model = XLNetForSequenceClassification.from_pretrained(model_path)
model.eval()

tokenizer = XLNetTokenizer.from_pretrained(model_path)

# Label list (same as before)
labels = [ 'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
           'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
           'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude',
           'grief', 'joy', 'love', 'nervousness', 'optimism', 'pride',
           'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral' ]


def predict_emotion(text):
    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding='max_length', max_length=64)
    
    # Run through model
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.sigmoid(logits).squeeze()

    # Get top predicted label
    top_indices = torch.topk(probs, k=3).indices.tolist()  # Top 3 emotions
    top_emotions = [(labels[i], round(probs[i].item(), 3)) for i in top_indices]

    return top_emotions


# 🔍 Example usage
if __name__ == "__main__":
    user_input = input("Enter a journal sentence: ")
    predictions = predict_emotion(user_input)
    print("\nPredicted Emotions:")
    for label, score in predictions:
        print(f"{label}: {score}")
