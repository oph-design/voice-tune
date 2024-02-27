import vertexai
from vertexai.generative_models import GenerativeModel, Part

def init_generative_model(project_id: str, location: str):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    multimodal_model = GenerativeModel("gemini-1.0-pro-001")

    return multimodal_model


def query_model(model, text_query) -> str:
    response = model.generate_content(
        [
            Part.from_text(text_query)
        ]
    )
    return response.text
