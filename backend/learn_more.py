import os
import requests
from dotenv import load_dotenv


def generate_summary_from_transcript(transcript: str) -> str:
    """
    Generates a concise title and summary from a given transcript using Hugging Face API.
    Returns the generated response as a string.
    """
    # Load environment variables
    load_dotenv()

    # Hugging Face API Key
    API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    if not API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY is not set in environment variables.")

    # Hugging Face API settings
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}

    # Create the API request prompt
    prompt = f"""
    You are an AI assistant that summarizes transcripts into a compelling and neutral title (3 words or less) and a brief description.

    Based on the following transcript, generate a *concise and informative title* along with a *description* summarizing the topic.

    After that provide 2 lines on why this topic is politically contended.

    Transcript:
    {transcript}

    """

    # Send request to Hugging Face API
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

    if response.status_code == 200:
        result = response.json()
        generated_text = result[0]['generated_text']
        trimmed_response = generated_text[len(prompt):].strip()
        # prompt = f"""
        # Beautify the text below and remove the prompt and the transcript sentence:
        #
        # Text:
        # {generated_text}
        # """
        # response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        # result = response.json()
        # generated_text = result[0]['generated_text']
        # if "xample:" in generated_text or "Title:" in generated_text:
        #     trimmed_response = generated_text.split("xample:")[-1].strip()
        #     trimmed_response = trimmed_response.split("Title:")[-1].strip()
        #     trimmed_response = trimmed_response.split(f"{transcript}")[-1].strip()
        #     last_occurrence_index = trimmed_response.rfind(transcript)
        #
        #     # If transcript is found, extract everything after it
        #     if last_occurrence_index != -1:
        #         trimmed_response = trimmed_response[last_occurrence_index + len(transcript):].strip()
        #     else:
        #         trimmed_response = trimmed_response.strip()
        # else:
        #     trimmed_response = generated_text.strip()

        return trimmed_response
    else:
        return f"Error {response.status_code}: {response.text}"


print(generate_summary_from_transcript("""The debate over healthcare policy in the United States remains a contentious issue among lawmakers. Proponents of a universal healthcare system argue that access to medical services is a fundamental human right and that a single-payer system would reduce costs and improve outcomes. On the other hand, opponents contend that government-run healthcare would lead to inefficiencies, higher taxes, and reduced quality of care. The discussion has intensified with recent legislative proposals seeking to expand Medicaid and Medicare, while critics warn of potential economic burdens and reduced incentives for medical innovation. With public opinion deeply divided, the future of American healthcare policy remains uncertain."""))