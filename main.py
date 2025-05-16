import requests
import time

# API key and endpoints
api_key = "3fgF91ECv9bkfYeFiB6WFkUi98byfSu2YyofXx6M"
upload_url = "https://api.json2video.com/v2/assets"
render_url = "https://api.json2video.com/v2/videos"
image_path = "D:\Others\image2video\kitten.jpg"
output_path = "kitten_video.mp4"

# Step 1: Upload image
with open(image_path, "rb") as image_file:
    upload_response = requests.post(
        upload_url,
        headers={"x-api-key": api_key},
        files={"file": image_file}
    )

if upload_response.status_code != 200:
    print(f"Upload failed: {upload_response.text}")
    exit()

image_url = upload_response.json()["url"]
print(f"Image uploaded: {image_url}")

# Step 2: Submit rendering job
template = {
    "template": {
        "duration": 10,
        "resolution": "hd",
        "scenes": [
            {
                "elements": [
                    {
                        "type": "image",
                        "src": image_url,
                        "duration": 10,
                        "animation": {"type": "zoom-in", "duration": 10}
                    }
                ]
            }
        ]
    }
}

render_response = requests.post(
    render_url,
    headers={"x-api-key": api_key, "Content-Type": "application/json"},
    json=template
)

if render_response.status_code != 200:
    print(f"Rendering failed: {render_response.text}")
    exit()

video_id = render_response.json()["id"]
print(f"Video rendering started: {video_id}")

# Step 3: Check status
status_url = f"https://api.json2video.com/v2/videos/{video_id}"
while True:
    status_response = requests.get(status_url, headers={"x-api-key": api_key})
    if status_response.status_code == 200:
        status = status_response.json()["status"]
        print(f"Status: {status}")
        if status == "completed":
            video_url = status_response.json()["url"]
            print(f"Video ready: {video_url}")
            break
        elif status == "failed":
            print(f"Rendering failed: {status_response.json()['error']}")
            break
    else:
        print(f"Status check failed: {status_response.text}")
        break
    time.sleep(10)

# Step 4: Download video
if status == "completed":
    video_response = requests.get(video_url)
    if video_response.status_code == 200:
        with open(output_path, "wb") as video_file:
            video_file.write(video_response.content)
        print(f"Video downloaded to {output_path}")
    else:
        print(f"Download failed: {video_response.text}")