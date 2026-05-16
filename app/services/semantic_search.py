def search_assessments(query, assessments, top_k=5):
    query = query.lower()

    scored = []

    for assessment in assessments:
        text = (
            assessment.get("name", "") + " " +
            assessment.get("description", "") + " " +
            assessment.get("test_type", "")
        ).lower()

        score = sum(word in text for word in query.split())

        scored.append((score, assessment))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [item[1] for item in scored[:top_k]]