import numpy as np
from const import signed_score



def test(model, data):
    scores = []

    for article in data:
        result = model.analyze_aspects(article["body"])
        vector = [signed_score(result[aspect]["label"], result[aspect]["score"]) for aspect in model.aspects]



        vector = np.array(vector, dtype=object)
        article_scores = []

        for i in range(len(model.aspects)):
            if vector[i] is not None:
                expected_correlations = model.aspect_correlation_matrix[i]

                mask = [(vector[j] is not None and not np.isnan(expected_correlations[j])) for j in range(len(model.aspects))]

                if sum(mask) < 2:
                    continue

                observed = vector[mask]
                expected = expected_correlations[mask]

                # Normalize observed vector to [-1, 1]
                if np.max(np.abs(observed)) == 0:
                    continue
                observed_norm = observed / np.max(np.abs(observed))

                # Cosine similarity between expected correlations and observed pattern
                sim = np.dot(observed_norm, expected) / (
                    np.linalg.norm(observed_norm) * np.linalg.norm(expected)
                )

                article_scores.append(sim)

        if article_scores:
            scores.append(np.mean(article_scores))

    # 4. Final crude accuracy
    if scores:
        return np.mean(scores)

    return None