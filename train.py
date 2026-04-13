import re
import spacy
from textblob import TextBlob
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification



# spaCy model
sp = spacy.load("en_core_web_sm")



# Pre-training HuggingFaces DeBERTa model
model_name = "yangheng/deberta-v3-base-absa-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)



file = open("./test/article_1.txt", "r", encoding="utf-8")
file_full = file.read()

file_text_start = "<text>"
file_text_end = "</text>"

file_text_start_index = file_full.find(file_text_start) + len(file_text_start)
file_text_end_index = file_full.find(file_text_end)

file_text = file_full[file_text_start_index:file_text_end_index]



# Pre-set list of aspects to parse for
aspects_list = ["Black Lives Matter", "BLM", "ABCDEFG"]



# Dictionary mapping labels to scores for overall sentiment calculation
label_score_dict = {
    "Negative": -1,
    "Neutral": 0,
    "Positive": 1
}



# Calculates overall sentiment from list of sentiments
# Finds the direction of the sentiments as well as calculated confidence
# Returns couple of label and score
def calculate_overall_sentiment(sentiments):
    if not sentiments:
        return None, None

    weighted_score = 0.0
    total_score = 0.0

    for sentiment in sentiments:
        weighted_score += label_score_dict[sentiment["label"]] * sentiment["score"]
        total_score += sentiment["score"]

    direction = weighted_score / total_score
    score = total_score / len(sentiments)

    if direction > 0.2:
        return "Positive", score
    elif direction < -0.2:
        return "Negative", score
    else:
        return "Neutral", score




# Analyze each aspect against the text
# Returns sentiments of structure:
# {
#   "found": True/False,
#   "sentence": str,
#   "sentiment": str
# }
def analyze_aspects(text, aspects):
    result = {}
    doc = sp(text)

    for aspect in aspects:
        sentiments = []
        aspect_lower = aspect.lower()

        # Search each sentence for the aspect
        for sentence in doc.sents:
            sentence_text = sentence.text
            if aspect_lower in sentence_text.lower():
                found = True
                sentiment = classifier(sentence_text, text_pair=aspect)
                sentiments.append(sentiment[0])

        label, score = determine_overall_sentiment(sentiments)
        result[aspect] = {
            "found": len(sentiments) > 0,
            "label": label,
            "score": score,
            "sentiments": sentiments
        }


    return result


sentiments = analyze_aspects(file_text, aspects_list)
print(sentiments)