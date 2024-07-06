import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import google.generativeai as genai
from googletrans import Translator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Gemini API
GOOGLE_API_KEY = 'AIzaSyDmRmD7N0ARGlugdu6ThwxlnhiXQ0qu7AA'
genai.configure(api_key=GOOGLE_API_KEY)

# Create a requests session with retry strategy
session = requests.Session()
retry = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Initialize the Google Translate API translator
translator = Translator()

# Define the character and tone for generating responses
CHARACTER_PROMPT = """
You are an assistat in an application that is the marketplace for secod hand used goods such as phoes , cloths and cars.you are supposed to get a prompt from the user stating their itention to create an ad to sell their goods, and then i turn suggest a title, description that is proper for them annd hass all the keywords it should
"""

# Function to generate a response using Gemini API with a preset character and tone
def generate_response(user_message):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = CHARACTER_PROMPT + "\n\nUser: " + user_message + "\nAssistant:"
    
    try:
        # Generate content with streaming enabled
        response = model.generate_content(prompt, stream=True)

        # Accumulate chunks of response text
        response_text = ""
        for chunk in response:
            response_text += chunk.text

        # Resolve the response to finalize attributes
        response.resolve()

        # Choose the best candidate (here, just choosing the first one)
        if response.candidates:
            candidate = response.candidates[0]
            if candidate.content:
                return candidate.content.parts[0].text.strip()

    except Exception as e:
        logging.error(f"Failed to generate response: {e}")

    return "I'm sorry, I couldn't generate a suitable response at the moment."

# Function to translate text to Persian
def translate_to_persian(text):
    try:
        translation = translator.translate(text, dest='fa')
        return translation.text
    except Exception as e:
        logging.error(f"Failed to translate text: {e}")
        return "I'm sorry, I couldn't translate the response at the moment."

# Function to generate ad suggestions (titles and descriptions) and translate to Persian
def generate_ad_suggestions(item_description):
    user_message = f"Please suggest an ad title and description for the following item: {item_description}"
    response = generate_response(user_message)
    translated_response = translate_to_persian(response)
    return translated_response

# Example usage
if __name__ == '__main__':
    item_description = "من یک تلفن همراه سامسونگ گلکسی S21 برای فروش دارم. عنوان و توضیحات مناسب برای آگهی را پیشنهاد دهید."
    suggestions = generate_ad_suggestions(item_description)
    print("Generated Ad Suggestions (Translated to Persian):")
    print(suggestions)
