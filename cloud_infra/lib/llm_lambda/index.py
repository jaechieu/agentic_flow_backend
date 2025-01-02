import json

def get_cors_headers():
    return {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Origin": "*",
    }

def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            **get_cors_headers(),
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return create_response(200, "")

    if event.get('httpMethod') == 'GET' and event.get('path') == '/node-types':
        node_types = [
            {"id": "Prompt", "name": "Prompt Node"},
            {"id": "LLM", "name": "LLM Node"},
            {"id": "Tool", "name": "Tool Node"},
            {"id": "Chain", "name": "Chain Node"},
        ]
        return create_response(200, node_types)

    return create_response(404, {"error": "Not found"})
