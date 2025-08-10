# FastAPI backend for sentiment analysis using Mistral via Ollama
# Returns "Positive", "Negative", or "Neutral" with robust error handling.
# Also provides brief explanations for the classification.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import requests
import logging

# -----------------------------------------------------------------------------
# Setup Logging
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Initialize FastAPI App
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Sentiment Analyzer API",
    description="Classify sentiment using Mistral via Ollama — runs locally.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Enable CORS for Streamlit
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Request Models
# -----------------------------------------------------------------------------
class SentimentRequest(BaseModel):
    """
    Schema for sentiment analysis requests.
    Ensures input is valid before processing.
    """
    text: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Text to analyze for sentiment"
    )


class ExplanationRequest(BaseModel):
    """
    Schema for explanation requests.
    Requires both original text and predicted sentiment.
    """
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Original text that was analyzed"
    )
    sentiment: str = Field( # type: ignore
        ...,
        pattern="^(Positive|Negative|Neutral)$",
        description="Predicted sentiment to explain"
    )

# -----------------------------------------------------------------------------
# Health Check
# -----------------------------------------------------------------------------
@app.get("/health")
def health():
    """
    Health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "model": "mistral"}

# -----------------------------------------------------------------------------
# Sentiment Analysis Endpoint
# -----------------------------------------------------------------------------
@app.post("/analyze/")
def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of input text using Mistral.
    Forces strict output: 'Positive', 'Negative', or 'Neutral'

    Args:
        request (SentimentRequest): Validated input containing 'text'

    Returns:
        dict: {"sentiment": "Positive|Negative|Neutral"}
    """
    input_text = request.text.strip()
    logger.info("Received sentiment analysis request")

    # ✅ Strict Prompt to Force Valid Output
    prompt = f"""
You are a sentiment classification engine. Analyze the following text and respond
with ONLY one word: 'Positive', 'Negative', or 'Neutral'.

If the text contains no meaningful language (e.g., numbers, symbols, codes),
respond with 'Neutral'.

Text:
\"\"\"
{input_text}
\"\"\"

Sentiment:
""".strip()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code != 200:
            logger.error(f"Mistral error {response.status_code}: {response.text}")
            raise HTTPException(status_code=502, detail="Error from Ollama")

        result = response.json()
        raw_sentiment = result.get("response", "").strip()

        # ✅ Normalize output
        if not raw_sentiment:
            raise HTTPException(status_code=500, detail="Empty response from model")

        # Extract first word and normalize
        predicted = raw_sentiment.split()[0].capitalize()

        if predicted not in ["Positive", "Negative", "Neutral"]:
            logger.warning(f"Model returned invalid sentiment: {predicted}")
            predicted = "Neutral"  # Conservative fallback

        logger.info(f"Sentiment: {predicted}")
        return {"sentiment": predicted}

    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama")
        raise HTTPException(
            status_code=503,
            detail="Cannot reach Ollama. Is it running?"
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Request timed out. Try shorter input."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# -----------------------------------------------------------------------------
# Explanation Endpoint
# -----------------------------------------------------------------------------
@app.post("/explain/")
def explain_sentiment(data: ExplanationRequest):
    """
    Generate a brief explanation for why the sentiment was classified as it is.

    Args:
        data (ExplanationRequest): Contains 'text' and 'sentiment'

    Returns:
        dict: {"explanation": "short sentence explaining the classification"}
    """
    input_text = data.text.strip()
    predicted_sentiment = data.sentiment.strip()

    prompt = f"""
Explain in one short sentence why the following text might be considered {predicted_sentiment} in sentiment.
Focus on tone, words, or context that support this label.

Text:
\"\"\"
{input_text}
\"\"\"

Explanation:
""".strip()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code != 200:
            logger.error(f"Ollama error {response.status_code}: {response.text}")
            raise HTTPException(status_code=502, detail="Error from Ollama during explanation")

        result = response.json()
        explanation = result.get("response", "").strip()

        if not explanation:
            return {"explanation": "No explanation available."}

        # Clean up: take only the first sentence
        explanation = explanation.split('.')[0].strip() + "."

        logger.info("Generated explanation successfully")
        return {"explanation": explanation}

    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama for explanation")
        return {"explanation": "Could not generate explanation (Ollama not reachable)."}
    except requests.exceptions.Timeout:
        logger.error("Explanation request timed out")
        return {"explanation": "Explanation generation timed out."}
    except Exception as e:
        logger.error(f"Unexpected error during explanation: {e}")
        return {"explanation": "Could not generate explanation."}