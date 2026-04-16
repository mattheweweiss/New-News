from const import signed_score



def train(model, data):
    # Storing vectors containing aspect-based sentiment analysis data
    vectors = []


    for article in data:
        result = model.analyze_aspects(article["body"])
        vector = [signed_score(result[aspect]["label"], result[aspect]["score"]) for aspect in model.aspects]
        vectors.append(vector)

    model.compute_correlations(vectors)