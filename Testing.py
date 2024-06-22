import requests
import json

# Define the API endpoint URL
url = "http://localhost:1337/v1/chat/completions"

# Define the request headers
headers = {
    'Content-Type': 'application/json'
}

# Define the JSON body of the request
data = {
  "messages": [
    {
      "content": "You are a helpful assistant.",
      "role": "system"
    },
    {
      "content": "Hello!",
      "role": "user"
    }
  ],
  "model": "mistral-ins-7b-q4",
  "stream": True,
  "max_tokens": 2048,
  "stop": [
    "hello"
  ],
  "frequency_penalty": 0,
  "presence_penalty": 0,
  "temperature": 0.7,
  "top_p": 0.95
}

# Convert the dictionary to a JSON string
json_data = json.dumps(data)

# Make the POST request
response = requests.post(url, headers=headers, data=json_data)

# Print response details for debugging
print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response Text:", response.text)

# Check the response status code
if response.status_code == 200:
    print(response.json())
    collected_content = []

    # Stream the response
    for line in response.iter_lines():
        if line:
            # Decode the JSON line
            line = line.decode('utf-8')
            if line.startswith("data:"):
                line = line[5:].strip()
                try:
                    json_data = json.loads(line)
                    delta = json_data['choices'][0]['delta']
                    if 'content' in delta:
                        collected_content.append(delta['content'])
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {line}")
    print(' '.join(collected_content))
    # Print the final collected content
    print('Final content:', ' '.join(collected_content))
else:
    print(f"Failed to call API. Status code: {response.status_code}, Response: {response.text}")