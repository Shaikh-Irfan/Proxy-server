#!/usr/bin/env python3
"""Simple CORS proxy for Gotenberg - Deploy on Render"""

from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

GOTENBERG_URL = os.environ.get('GOTENBERG_URL', 'https://gotenberg-7-kyix.onrender.com')

def forward_request(endpoint):
    try:
        # Read all files from the request
        files = {}
        for key, file in request.files.items():
            files[key] = (file.filename, file.read(), file.content_type)
        
        response = requests.post(
            f'{GOTENBERG_URL}{endpoint}',
            files=files,
            timeout=120
        )
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/pdf')
        )
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)

@app.route('/forms/libreoffice/convert', methods=['POST', 'OPTIONS'])
def libreoffice():
    if request.method == 'OPTIONS':
        return Response(status=200)
    return forward_request('/forms/libreoffice/convert')

@app.route('/forms/chromium/convert', methods=['POST', 'OPTIONS'])
def chromium():
    if request.method == 'OPTIONS':
        return Response(status=200)
    return forward_request('/forms/chromium/convert')

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
