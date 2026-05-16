def get_recommendations(user_query, assessments):

    user_query = user_query.lower()
  

    matched_assessments = []

    for assessment in assessments:

        name = assessment["name"].lower()
        description = assessment["description"].lower()
        test_type = assessment.get("test_type", "").lower()

        if (
            user_query in name
            or user_query in description
            or user_query in test_type
        ):
            matched_assessments.append(assessment)

    return matched_assessments



def needs_clarification(user_query):

    vague_queries = [
        "assessment",
        "test",
        "job",
        "hiring",
        "candidate"
    ]

    user_query = user_query.lower()

    return user_query in vague_queries


def is_conversation_complete(user_query):

    user_query = user_query.lower()

    completion_words = [
        "thanks",
        "thank you",
        "bye",
        "done",
        "that's all",
        "ok thanks",
        "great thanks"
    ]

    for word in completion_words:

        if word in user_query:
            return True

    return False

def should_refuse_query(user_query):

    user_query = user_query.lower()

    unrelated_keywords = [
        "weather",
        "joke",
        "movie",
        "ipl",
        "cricket",
        "football",
        "news",
        "recipe",
        "song"
    ]

    for word in unrelated_keywords:

        if word in user_query:
            return True

    return False