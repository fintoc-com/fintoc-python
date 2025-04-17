import os

from flask import Flask, request

from fintoc.webhook import WebhookSignature
from fintoc.errors import WebhookSignatureError

app = Flask(__name__)

# Find your endpoint's secret in your webhook settings in the Fintoc Dashboard
WEBHOOK_SECRET = os.getenv('FINTOC_WEBHOOK_SECRET')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Handle incoming webhooks from Fintoc.

    Validates the webhook signature and processes the payload if valid.
    """
    # Get the signature header
    signature = request.headers.get('Fintoc-Signature')
    if not signature:
        return 'No signature header', 400

    # Get the raw request payload
    payload = request.get_data().decode('utf-8')

    try:
        # Verify the webhook signature
        WebhookSignature.verify_header(
            payload=payload,
            header=signature,
            secret=WEBHOOK_SECRET
        )

        # If verification passes, process the webhook
        data = request.json

        # Here you can handle different webhook types
        webhook_type = data.get('type')
        if webhook_type == 'payment_intent.succeeded':
            print('Payment was succeeded!')
        elif webhook_type == 'payment_intent.failed':
            print('Payment failed')
        # Add more webhook types as needed

        return 'success', 200

    except WebhookSignatureError as e:
        print('Invalid signature!')
        return str(e), 400
    except Exception as e:
        return 'Internal server error', 500

if __name__ == '__main__':
    # For development only - use proper WSGI server in production
    app.run(port=5000, debug=True)
