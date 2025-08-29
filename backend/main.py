from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import groq
import time
import random
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# List of random topics and styles for generation
RANDOM_TOPICS = [
    "a personal portfolio for a digital artist",
    "a restaurant website with online ordering",
    "a travel blog about hidden gems",
    "a tech startup landing page",
    "a photography portfolio",
    "an e-commerce site for handmade crafts",
    "a fitness coach's website",
    "a music band's official site",
    "a recipe blog",
    "a pet adoption platform"
]

STYLES = [
    "minimalist",
    "modern",
    "retro",
    "futuristic",
    "corporate",
    "playful",
    "elegant",
    "bold",
    "clean",
    "colorful"
]

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
DAILY_LIMIT = 100
counter = {"count": 0, "reset_time": time.time() + 86400}

class GenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = None

@app.get("/")
async def read_root():
    return {
        "message": "Non-deterministic Website Generator API",
        "endpoints": {
            "GET /random": "Get a random website",
            "POST /generate": "Generate a website with custom prompt"
        }
    }

@app.get("/random")
async def generate_random_website():
    """Generate a website with random topic and style."""
    random_data = get_random_prompt()
    request = GenerationRequest(**random_data)
    return await generate_website(request)

def get_random_prompt() -> Dict[str, str]:
    """Generate a random prompt and style combination."""
    return {
        "prompt": random.choice(RANDOM_TOPICS),
        "style": random.choice(STYLES)
    }

@app.post("/generate")
async def generate_website(request: GenerationRequest):
    global counter
    now = time.time()

    # Reset daily counter if needed
    if now > counter["reset_time"]:
        counter = {"count": 0, "reset_time": now + 86400}

    # Check rate limit
    if counter["count"] >= DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit of {DAILY_LIMIT} websites reached. Try again tomorrow."
        )
        
    # If no prompt is provided, generate a random one
    if not request.prompt:
        random_data = get_random_prompt()
        request.prompt = random_data["prompt"]
        request.style = random_data["style"]

    # Initialize Groq client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: GROQ_API_KEY not set"
        )
    
    client = groq.Groq(api_key=api_key)

    try:
        # Prepare the prompt with optional style
        prompt_text = f"Generate a unique, modern, and responsive HTML/CSS website about: {request.prompt}"
        if request.style:
            prompt_text += f" in {request.style} style"
        
        # Call Groq API
        response = client.chat.completions.create(
            model="compound-beta",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional web designer. Generate clean, responsive HTML/CSS websites."
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            temperature=0.9,
            max_tokens=2000
        )

        # Update counter
        counter["count"] += 1

        # Extract HTML content from the response
        html_content = response.choices[0].message.content
        
        # Clean up the response if it contains markdown code blocks
        if "```html" in html_content:
            html_content = html_content.split("```html")[1].split("```")[0].strip()
        elif "```" in html_content:
            parts = html_content.split("```")
            # Get the first code block's content
            if len(parts) > 1:
                html_content = parts[1].strip()

        return {
            "html": html_content,
            "remaining": max(0, DAILY_LIMIT - counter["count"]),
            "reset_time": counter["reset_time"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
