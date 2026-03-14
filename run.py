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
aspects_list = ["Black Lives Matter", "black lives matter", "BLM", "blm"]



# Finds aspect in file text
# If not found, returns false, otherwise true
def find_aspect(aspect):
    if file_text.find(aspect) == -1:
        return False
    else:
        return True



# Creates list of aspects used in text
used_aspects = [x for x in filter(find_aspect, aspects_list)]



# Analyze each aspect against the text 
def analyze_aspects(text, aspects):
    sentiments = {}

    for aspect in aspects:
        sentiment = classifier(text, text_pair=aspect)
        sentiments[aspect] = sentiment

    return sentiments


sentiments = analyze_aspects(file_text, used_aspects)
print(sentiments)