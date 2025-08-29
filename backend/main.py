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

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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
        prompt_text = """Create a vibrant, colorful one-page website about an interesting topic of your choice.
        
        Requirements:
        1. Create a single-page website with 1-2 main sections
        2. Use bright, vibrant colors and gradients
        3. No placeholders or lorem ipsum - generate real content
        4. Make it visually appealing with CSS (no images)
        5. Include:
           - A catchy headline
           - 1-2 paragraphs of engaging content
           - Some styled text elements (quotes, highlights, etc.)
           - A simple footer
        6. Keep the design clean and modern
        7. Make it responsive for all screen sizes
        """
        
        if request.style:
            prompt_text += f"\n        Style: {request.style.capitalize()} aesthetic with vibrant colors"
        
        # Call Groq API
        response = client.chat.completions.create(
            model="compound-beta",
            messages=[
                {
                    "role": "system",
                    "content": """You are a professional web designer and content creator. Generate a complete, content-rich, responsive HTML/CSS website with the following requirements:
                    1. Create a full website with multiple sections (header, main content with at least 3 sections, footer)
                    2. Include detailed, well-written content about the topic (no lorem ipsum)
                    3. Use semantic HTML5 elements (header, nav, main, section, article, footer)
                    4. Create a professional color scheme and typography
                    5. Make it fully responsive for all screen sizes
                    6. Include interactive elements like buttons or links
                    7. No placeholder text or images - use only text and CSS for visual elements
                    8. Ensure the content is well-structured and informative
                    9. Include at least 3 different sections with unique content
                    10. Add a footer with relevant links and information
                    
                    The website should look like a complete, professional site, not just a template."""
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
