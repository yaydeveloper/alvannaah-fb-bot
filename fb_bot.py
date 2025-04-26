from flask import Flask, request
import requests
import random
import json

app = Flask(__name__)

# Facebook Page Access Token (replace with your token)
PAGE_ACCESS_TOKEN = 'YOUR_PAGE_ACCESS_TOKEN_HERE'

# List of ImgBB URLs (replace with your URLs)
IMAGE_URLS = [
    'https://i.ibb.co/image1/image.jpg',
    'https://i.ibb.co/image2/image.jpg',
    # Add your 10,000+ ImgBB URLs here
]

# Verify token for webhook setup
VERIFY_TOKEN = 'your_verify_token_123'

# Send message/image to user
def send_message(recipient_id, message_type, content):
    url = f'https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    if message_type == 'text':
        data = {
            'recipient': {'id': recipient_id},
            'message': {'text': content}
        }
    elif message_type == 'image':
        data = {
            'recipient': {'id': recipient_id},
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {'url': content}
                }
            }
        }
    requests.post(url, json=data)

# Webhook verification
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Error, wrong token', 403

# Handle incoming messages
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for event in entry['messaging']:
                if 'message' in event and 'text' in event['message']:
                    sender_id = event['sender']['id']
                    message_text = event['message']['text'].lower()
                    if 'tamanna' in message_text:
                        if IMAGE_URLS:
                            random_image = random.choice(IMAGE_URLS)
                            send_message(sender_id, 'image', random_image)
                            send_message(sender_id, 'text', "Here's a random Tamannaah Bhatia image! ✨")
                        else:
                            send_message(sender_id, 'text', "No images available yet.")
                    else:
                        send_message(sender_id, 'text', "Please type 'tamanna' to get a random image!")
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)