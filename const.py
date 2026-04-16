# Dictionary mapping labels to scores for overall sentiment calculation
label_score_dict = {
    "Negative": -1,
    "Neutral": 0,
    "Positive": 1
}


# Gets sign from score (converts positive score to label * score)
# Returns None if label and score do not exist
def signed_score(label, score):
    return label_score_dict[label] * score if label is not None and score is not None else None