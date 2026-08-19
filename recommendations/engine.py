import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from services.models import Service

def get_recommendations(service_id, top_n=5):
    services = Service.objects.filter(is_available=True).select_related('category')

    if not services.exists():
        return []

    # Build a DataFrame from service data
    data = []
    for s in services:
        category_name = s.category.name if s.category else ''
        # Combine category + description into one text field for similarity comparison
        combined_text = f"{category_name} {s.description}"
        data.append({
            'id': s.id,
            'title': s.title,
            'price': float(s.price),
            'combined_text': combined_text
        })

    df = pd.DataFrame(data)

    if service_id not in df['id'].values:
        return []

    # Convert text into TF-IDF vectors (numeric representation of text similarity)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])

    # Compute similarity between all services
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Find the row index for our target service
    idx = df.index[df['id'] == service_id][0]

    # Get similarity scores for this service against all others, sorted descending
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Skip the first result (it's the service itself, always 100% similar to itself)
    top_matches = similarity_scores[1:top_n + 1]

    recommended_ids = [df.iloc[i]['id'] for i, score in top_matches]
    return list(Service.objects.filter(id__in=recommended_ids))