from transformers import pipeline
from bertopic import BERTopic
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from umap import UMAP

# Load the zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Labels for classification
labels = ["progressive policies", "conservative policies", "neutral"]


def get_top_k_similar(vector, all_vectors, k=5):
    """
    Finds the top k most similar vectors using cosine similarity.

    :param vector: The target vector (shape: 1 x embedding_dim)
    :param all_vectors: A 2D NumPy array of shape (n_samples, embedding_dim)
    :param k: Number of top similar vectors to retrieve
    :return: Indices of the top k similar vectors
    """
    # Compute cosine similarity between target vector and all others
    similarities = cosine_similarity(vector.reshape(1, -1), all_vectors).flatten()

    # Get top k indices (excluding the first if it's the same transcript)
    top_k_indices = np.argsort(similarities)[::-1][:k]

    #get_pole_ids(), get_bias_scores(), find biggest difference in bias and return

    return top_k_indices

def get_bias_score(text):
    result = classifier(text, labels)

    # Extract scores
    scores = {label: score for label, score in zip(result["labels"], result["scores"])}

    # Compute bias score: left (-1), right (+1), neutral (0)
    bias_score = scores["conservative policies"] - scores["progressive policies"]

    return bias_score

def calculate_user_bias(current_user_bias, pole_bias, user_num_poles):
    #mark as visited before calling this function
    alpha = 1/(user_num_poles + 1)
    new_user_bias = (1-alpha) * current_user_bias + alpha * pole_bias
    return new_user_bias






# Sample political transcripts
transcripts = [
    "We need higher taxes on corporations to support social programs.",  # Expected: Left (-)
    "The free market should be left alone with minimal government interference.",  # Expected: Right (+)
    "Both parties need to work together to solve economic issues.",  # Expected: Neutral (0)
]

# Test each transcript
for i, transcript in enumerate(transcripts, 1):
    score = get_bias_score(transcript)
    print(f"Transcript {i}: Bias Score = {score:.2f}")


topic_model = BERTopic()
transcripts1 = [
    # Economy
    "We need higher taxes on corporations to support social programs.",
    "Lowering taxes will help businesses grow and create more jobs.",
    "Government spending should be reduced to balance the budget.",
    "A strong middle class is the backbone of a thriving economy.",
    "Universal basic income could help reduce poverty and stabilize the economy.",

    # Healthcare
    "Healthcare should be free and accessible to all citizens.",
    "Private healthcare provides better services than government-run programs.",
    "Pharmaceutical companies need stricter regulations to control drug prices.",
    "Universal healthcare would reduce medical bankruptcy cases.",
    "The government should not interfere in private healthcare decisions.",

    # Immigration
    "We need stronger border security to prevent illegal immigration.",
    "Immigrants contribute positively to the economy and society.",
    "There should be a path to citizenship for undocumented immigrants.",
    "Illegal immigration strains public resources and should be controlled.",
    "A fair immigration system ensures economic growth and social stability.",

    # Foreign Policy
    "The US should increase military funding to maintain global dominance.",
    "Diplomacy is the best way to resolve international conflicts.",
    "Trade sanctions should be used to pressure authoritarian regimes.",
    "America should reduce foreign military interventions.",
    "Our alliances with democratic nations must be strengthened.",

    # Education
    "Public universities should be tuition-free for low-income students.",
    "School choice programs empower parents to pick the best education for their kids.",
    "Standardized testing is not an accurate measure of student success.",
    "Teachers should be paid more to improve education quality.",
    "More funding is needed for STEM programs in public schools.",

    # Climate Change
    "The government must take urgent action to combat climate change.",
    "Renewable energy is the key to a sustainable future.",
    "Fossil fuels are still necessary for economic growth.",
    "Regulations on carbon emissions hurt businesses and job growth.",
    "Climate policies should balance environmental and economic needs.",

    # Gun Control
    "Stronger gun control laws will reduce mass shootings.",
    "The Second Amendment protects the right to bear arms.",
    "Background checks should be mandatory for all gun purchases.",
    "Gun-free zones make people more vulnerable to attacks.",
    "Responsible gun ownership should be encouraged, not restricted.",

    # Social Issues
    "Affirmative action is necessary to ensure equal opportunities.",
    "Freedom of speech must be protected, even for controversial opinions.",
    "Systemic racism is a major issue that needs to be addressed.",
    "The death penalty should be abolished as it is inhumane.",
    "LGBTQ+ rights should be protected under federal law.",

    # Technology
    "Big tech companies should be broken up to prevent monopolies.",
    "Artificial intelligence will revolutionize the job market.",
    "Government regulation of social media platforms is necessary.",
    "Privacy rights are being eroded by mass surveillance programs.",
    "Cryptocurrency is the future of decentralized finance.",

    # National Security
    "Counterterrorism efforts must be strengthened to protect national security.",
    "Mass surveillance is a violation of personal freedoms.",
    "Cybersecurity should be a top priority for the government.",
    "Military expansion is necessary to maintain global stability.",
    "Terrorism is best fought through intelligence, not warfare."
]

# Train topic model
topics, _ = topic_model.fit_transform(transcripts1)

# Print topics
topic_info = topic_model.get_topic_info()

# Print each topic with its representative documents
for index, row in topic_info.iterrows():
    topic_number = row["Topic"]
    print(f"\n### Topic {topic_number}:")
    for doc in row["Representative_Docs"][:5]:  # Show only the first 5 docs
        print(f"- {doc}")
