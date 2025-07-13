import requests
import time

# ============================
# Replace with your own keys
# ============================
vision_key = 'YOUR_COGNITIVE_SERVICES_KEY'
vision_endpoint = 'https://YOUR_REGION.api.cognitive.microsoft.com/vision/v3.2/read/analyze'

translator_key = 'YOUR_TRANSLATOR_KEY'
translator_endpoint = 'https://api.cognitive.microsofttranslator.com'
translator_location = 'YOUR_RESOURCE_LOCATION'

# ============================
# Load Image
# ============================
image_path = 'test-image.jpg'
with open(image_path, 'rb') as f:
    image_data = f.read()

# ============================
# Step 1: Read Text from Image
# ============================
print("Sending image for OCR...")
vision_headers = {
    'Ocp-Apim-Subscription-Key': vision_key,
    'Content-Type': 'application/octet-stream'
}
vision_response = requests.post(vision_endpoint, headers=vision_headers, data=image_data)

# Get Operation URL
operation_url = vision_response.headers.get('Operation-Location')
if not operation_url:
    print("Failed to start OCR process. Check keys/endpoint.")
    exit()

# ============================
# Step 2: Wait and Fetch Result
# ============================
print("Waiting for OCR result...")
time.sleep(5)  # wait for processing
ocr_result = requests.get(operation_url, headers={'Ocp-Apim-Subscription-Key': vision_key}).json()

# Extract lines
lines = []
try:
    for line in ocr_result['analyzeResult']['readResults'][0]['lines']:
        lines.append(line['text'])
except Exception as e:
    print("OCR Extraction Failed:", e)
    exit()

text = ' '.join(lines)
print("Extracted Text:", text)

# ============================
# Step 3: Translate to Urdu
# ============================
print("Translating to Urdu...")
translate_path = '/translate?api-version=3.0&to=ur'
translate_headers = {
    'Ocp-Apim-Subscription-Key': translator_key,
    'Ocp-Apim-Subscription-Region': translator_location,
    'Content-Type': 'application/json'
}
translate_body = [{'text': text}]
translate_response = requests.post(
    translator_endpoint + translate_path,
    headers=translate_headers,
    json=translate_body
)

# Output translated text
try:
    translated_text = translate_response.json()[0]['translations'][0]['text']
    print("Translated Text (Urdu):", translated_text)
except:
    print("Translation Failed")
