import requests
import os
import json
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_image(prompt, api_key=None, width=1024, height=1024, model="flux", aspect_ratio="1:1"):
    """
    Generate an image using the AIGuruLab API
    
    Args:
        prompt (str): Text description of the image to generate
        api_key (str, optional): Your AIGuruLab API key. If None, loads from environment variable
        width (int): Image width in pixels
        height (int): Image height in pixels
        model (str): Model to use ('sdxl' or 'flux')
        aspect_ratio (str): Aspect ratio (only applicable for Flux model)
        
    Returns:
        str: Path to the saved image or None if failed
    """
    # Use API key from parameter or environment variable
    if api_key is None:
        api_key = os.getenv("API_KEY")
        if not api_key:
            print("Error: No API key provided and API_KEY not found in environment variables")
            return None
    
    BASE_URL = 'https://aigurulab.tech'
    
    payload = {
        'width': width,
        'height': height,
        'input': prompt,
        'model': model,
        'aspectRatio': aspect_ratio  # Applicable to Flux model only
    }
    
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"Sending request to {BASE_URL}/api/generate-image")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/generate-image", 
            json=payload,
            headers=headers
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
        
        # Parse the response JSON
        response_data = response.json()
        
        if "image" not in response_data:
            print("Error: No 'image' field in the response")
            print(f"Response: {response_data}")
            return None
        
        # Get the image URL
        image_url = response_data["image"]
        print(f"Image URL: {image_url}")
        
        # Download the image from the URL
        print(f"Downloading image from URL...")
        img_response = requests.get(image_url)
        
        if img_response.status_code != 200:
            print(f"Error downloading image: Status code {img_response.status_code}")
            return None
        
        # Save the image
        output_path = "generated_image.png"
        with open(output_path, "wb") as f:
            f.write(img_response.content)
        
        print(f"Image saved to {os.path.abspath(output_path)}")
        
        # Verify the image can be opened
        try:
            img = Image.open(output_path)
            print(f"Image verified: Size {img.size}, Mode {img.mode}")
            return output_path
        except Exception as e:
            print(f"Warning: Saved image cannot be opened with PIL: {e}")
            return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    # Example prompt
    prompt = "A very cute tuxedo cat gently eating raw egg yolk from a shallow white plate, indoors with soft natural lighting, cozy and warm atmosphere, close-up view focused on the cat's face and the plate."
    
    # Generate the image using API key from .env file
    image_path = generate_image(
        prompt=prompt,
        width=1024,
        height=1024,
        model="flux",
        aspect_ratio="1:1"
    )
    
    if image_path:
        print(f"Success! Image generated and saved to {image_path}")
    else:
        print("Failed to generate image")