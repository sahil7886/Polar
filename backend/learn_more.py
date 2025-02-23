from transformers import pipeline

# Load zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Example transcript
transcript = """The debate over gun control continues as lawmakers argue about the balance between Second Amendment rights and public safety measures..."""

# Candidate topics
candidate_labels = [
    "gun control", "healthcare", "climate change", "taxation",
    "free speech", "immigration", "abortion", "foreign policy",
    "criminal justice", "education policy", "economic policy"
]

# Classify the topic
result = classifier(transcript, candidate_labels)
topic = result["labels"][0]  # The most relevant topic

print("Identified Topic:", topic)
