import vertexai
from vertexai.generative_models import GenerativeModel, Part

# TODO (developer): update project id
vertexai.init(project="test-project-438414", location="us-central1")

model = GenerativeModel("gemini-1.5-flash-002")

contents = [
    # Text prompt
    "Summarize this video.",
    # YouTube video of Google Pixel 9
    Part.from_uri("https://youtu.be/MsAPm8TCFhU", "video/mp4"),
]

response = model.generate_content(contents)
print(response.text)    