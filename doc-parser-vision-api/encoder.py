import json
import base64
import os

# Your JSON data
data = {
}

# Convert JSON to string and then encode it to base64
json_str = json.dumps(data)
encoded_json = base64.b64encode(json_str.encode()).decode()

# Print encoded JSON
print(encoded_json)
