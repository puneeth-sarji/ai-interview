import google.generativeai as genai
import os

# Initialize Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Use the appropriate Gemini model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

async def analyze_code(code: str) -> str:
    """
    Sends the code to Gemini API for analysis and optimization feedback.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not configured."
        
    prompt = f"""
    Please analyze the following code snippet. 
    1. Identify any potential bugs or syntax errors.
    2. Discuss its time and space complexity.
    3. Suggest optimizations and best practices.
    
    Code:
    ```
    {code}
    ```
    """
    
    try:
        # In a real async environment, you might want to run this in a threadpool 
        # or use an async client if available for the generative AI SDK.
        # For simplicity, we use the synchronous generate_content.
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"
