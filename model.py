from const import label_score_dict
import csv
import numpy as np
from random import shuffle
import re
import spacy
from textblob import TextBlob
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification



class Model:

    def __init__(self, aspects):
        self.aspects = aspects

        # spaCy model
        self.sp = spacy.load("en_core_web_sm")
        # Pre-training HuggingFaces DeBERTa model
        model_name = "yangheng/deberta-v3-base-absa-v1.1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

        # Aspect correlation matrix
        try:
            self.aspect_correlation_matrix = np.load("aspect_correlation_matrix.npy")
        except:
            self.aspect_correlation_matrix = []


    # Calculates overall sentiment from list of sentiments
    # Finds the direction of the sentiments as well as calculated confidence
    # Returns couple of label and score
    def calculate_overall_sentiment(self, sentiments):

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
    def analyze_aspects(self, text):
        result = {}
        doc = self.sp(text)

        for aspect in self.aspects:
            sentiments = []
            aspect_lower = aspect.lower()

            # Search each sentence for the aspect
            for sentence in doc.sents:
                sentence_text = sentence.text
                if aspect_lower in sentence_text.lower():
                    sentiment = self.classifier(sentence_text, text_pair=aspect)
                    sentiments.append(sentiment[0])

            label, score = self.calculate_overall_sentiment(sentiments)
            result[aspect] = {
                "found": len(sentiments) > 0,
                "label": label,
                "score": score,
                "sentiments": sentiments
            }

        
        return result


    def masked_correlation(self, x, y):
        mask = [(a is not None and b is not None) for a, b in zip(x, y)]
        x_f = np.array([a for a, m in zip(x, mask) if m], dtype=float)
        y_f = np.array([b for b, m in zip(y, mask) if m], dtype=float)

        if len(x_f) < 2:
            return np.nan

        return np.corrcoef(x_f, y_f)[0, 1]


    def compute_correlations(self, vectors):
        vectors = np.array(vectors, dtype=object)
        n = vectors.shape[1]
        correlation = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                correlation[i, j] = self.masked_correlation(vectors[:, i], vectors[:, j])

        self.aspect_correlation_matrix = correlation
        np.save("aspect_correlation_matrix.npy", self.aspect_correlation_matrix)
        return correlation