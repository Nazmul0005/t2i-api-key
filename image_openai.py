import openai

openai.api_key = ""

response = openai.Image.create(
    prompt="A futuristic cityscape at sunset",
    n=1,
    size="1024x1024",
    model="dall-e-3"
)

image_url = response['data'][0]['url']
print(image_url)
