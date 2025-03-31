import os
import logging
import json
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Sample data to work with
sample_data = {
    "items": [
        {"id": 1, "name": "Item 1", "description": "This is item 1"},
        {"id": 2, "name": "Item 2", "description": "This is item 2"},
        {"id": 3, "name": "Item 3", "description": "This is item 3"}
    ]
}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/items', methods=['GET', 'OPTIONS'])
def get_items():
    """API endpoint to get all items"""
    # Log the request headers for debugging
    app.logger.debug(f"Request headers: {dict(request.headers)}")
    
    # Return all items
    response = jsonify(sample_data)
    
    # Add custom CORS headers to demonstrate their use
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    # Log the response headers for debugging
    app.logger.debug(f"Response headers: {dict(response.headers)}")
    
    return response

@app.route('/api/items/<int:item_id>', methods=['GET', 'OPTIONS'])
def get_item(item_id):
    """API endpoint to get a specific item by ID"""
    if request.method == 'OPTIONS':
        response = jsonify({"message": "CORS preflight request successful"})
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    for item in sample_data['items']:
        if item['id'] == item_id:
            response = jsonify(item)
            origin = request.headers.get('Origin', '*')
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
            
    response = jsonify({"error": "Item not found"})
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 404

@app.route('/api/items', methods=['POST', 'OPTIONS'])
def create_item():
    """API endpoint to create a new item"""
    if request.method == 'OPTIONS':
        response = jsonify({"message": "CORS preflight request successful"})
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    # Get the data from the request
    new_item = request.json
    
    # Validate the data
    if not new_item or 'name' not in new_item or 'description' not in new_item:
        response = jsonify({"error": "Invalid item data. 'name' and 'description' are required."})
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 400
    
    # Create a new ID
    new_id = max([item['id'] for item in sample_data['items']]) + 1
    
    # Create the new item
    item = {
        "id": new_id,
        "name": new_item['name'],
        "description": new_item['description']
    }
    
    # Add the item to the data
    sample_data['items'].append(item)
    
    # Return the new item
    response = jsonify(item)
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 201

@app.route('/api/items/<int:item_id>', methods=['PUT', 'OPTIONS'])
def update_item(item_id):
    """API endpoint to update an existing item"""
    if request.method == 'OPTIONS':
        response = jsonify({"message": "CORS preflight request successful"})
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    # Get the data from the request
    updated_item = request.json
    
    # Validate the data
    if not updated_item:
        response = jsonify({"error": "Invalid item data"})
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 400
    
    # Find the item
    for i, item in enumerate(sample_data['items']):
        if item['id'] == item_id:
            # Update the item
            if 'name' in updated_item:
                sample_data['items'][i]['name'] = updated_item['name']
            if 'description' in updated_item:
                sample_data['items'][i]['description'] = updated_item['description']
            
            # Return the updated item
            response = jsonify(sample_data['items'][i])
            origin = request.headers.get('Origin', '*')
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
    
    # If the item was not found
    response = jsonify({"error": "Item not found"})
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'PUT,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 404

@app.route('/api/items/<int:item_id>', methods=['DELETE', 'OPTIONS'])
def delete_item(item_id):
    """API endpoint to delete an item"""
    if request.method == 'OPTIONS':
        response = jsonify({"message": "CORS preflight request successful"})
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
        
    # Find the item
    for i, item in enumerate(sample_data['items']):
        if item['id'] == item_id:
            # Delete the item
            deleted_item = sample_data['items'].pop(i)
            
            # Return the deleted item
            response = jsonify(deleted_item)
            origin = request.headers.get('Origin', '*')
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
    
    # If the item was not found
    response = jsonify({"error": "Item not found"})
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 404

@app.route('/api/cors-test', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def cors_test():
    """API endpoint to test CORS with different HTTP methods"""
    # Log the request for debugging
    app.logger.debug(f"CORS test received {request.method} request")
    app.logger.debug(f"Request headers: {dict(request.headers)}")
    
    # If it's an OPTIONS request, return early with the appropriate headers
    if request.method == 'OPTIONS':
        response = jsonify({"message": "CORS preflight request successful"})
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        app.logger.debug(f"Response headers: {dict(response.headers)}")
        return response
        
    # If it's not an OPTIONS request, handle it based on the method
    method_responses = {
        'GET': {"message": "CORS GET request successful", "method": "GET"},
        'POST': {"message": "CORS POST request successful", "method": "POST", "body": request.json},
        'PUT': {"message": "CORS PUT request successful", "method": "PUT", "body": request.json},
        'DELETE': {"message": "CORS DELETE request successful", "method": "DELETE"}
    }
    
    # Get the appropriate response for the method
    response_data = method_responses.get(request.method, {"message": "Unknown method"})
    
    # Create the response
    response = jsonify(response_data)
    
    # Add custom CORS headers
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    # Log the response headers for debugging
    app.logger.debug(f"Response headers: {dict(response.headers)}")
    
    return response

@app.route('/api/echo-headers', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def echo_headers():
    """API endpoint to echo back all headers from the request"""
    # Create a dictionary of the headers
    headers_dict = dict(request.headers)
    
    # Create the response
    response = jsonify({
        "request_headers": headers_dict,
        "method": request.method,
        "url": request.url,
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.json if request.is_json else None
    })
    
    # Add custom CORS headers
    origin = request.headers.get('Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    return response
