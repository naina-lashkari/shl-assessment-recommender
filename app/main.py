from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.recommendation_engine import (
    get_recommendations,
    needs_clarification,
    is_conversation_complete,
    should_refuse_query
)

from app.services.semantic_search import search_assessments

from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation
)

from app.utils.loader import load_assessments


app = FastAPI()

# Load assessments once at startup
assessments = load_assessments()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "SHL Assessment Recommender API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    conversation_text = " ".join(
        [message.content for message in request.messages]
    )

    print(conversation_text)

    if should_refuse_query(conversation_text):

        return ChatResponse(
            reply="I can only help with SHL assessment recommendations.",
            recommendations=[],
            end_of_conversation=False
        )

    if needs_clarification(conversation_text):

        return ChatResponse(
            reply="Please specify the role or skills you are hiring for.",
            recommendations=[],
            end_of_conversation=False
        )

    if is_conversation_complete(conversation_text):

        return ChatResponse(
            reply="Glad I could help. Goodbye!",
            recommendations=[],
            end_of_conversation=True
        )

    matched_assessments = search_assessments(
        conversation_text,
        assessments
    )

    if not matched_assessments:

        return ChatResponse(
            reply="Sorry, I could not find matching SHL assessments.",
            recommendations=[],
            end_of_conversation=True
        )

    recommendations = []

    for assessment in matched_assessments:

        recommendations.append(
            Recommendation(
                name=assessment["name"],
                url=assessment["url"],
                test_type=assessment.get("test_type", "Not Available"),
                description=assessment["description"]
            )
        )

    return ChatResponse(
        reply=f"Found {len(recommendations)} matching SHL assessments for your query.",
        recommendations=recommendations,
        end_of_conversation=False
    )