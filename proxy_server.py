#!/usr/bin/env python3
"""Simple CORS proxy for Gotenberg - Deploy on Render"""

from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

GOTENBERG_URL = os.environ.get('GOTENBERG_URL', 'https://gotenberg-7-kyix.onrender.com')

@app.route('/forms/libreoffice/convert', methods=['POST'])
def libreoffice():
    try:
        response = requests.post(
            f'{GOTENBERG_URL}/forms/libreoffice/convert',
            files=request.files,
            timeout=120
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/pdf')
        )
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)

@app.route('/forms/chromium/convert', methods=['POST'])
def chromium():
    try:
        response = requests.post(
            f'{GOTENBERG_URL}/forms/chromium/convert',
            files=request.files,
            timeout=120
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/pdf')
        )
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

# Enable CORS for all routes
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)