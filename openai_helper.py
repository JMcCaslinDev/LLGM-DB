import requests
import json
from typing import List, Optional
from config import OPENAI_API_KEY, OPENAI_ORGANIZATION  # Make sure OPENAI_ORGANIZATION is in config.py

def generate_embedding(text: str, model: str = "text-embedding-ada-002") -> Optional[List[float]]:
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Organization": OPENAI_ORGANIZATION
    }

    payload = json.dumps({
        "input": text,
        "model": model
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = json.loads(response.text)
        embedding = data['data'][0]['embedding']
        return embedding
    else:
        print(f"Failed to generate embedding: {response.text}")
        return None
