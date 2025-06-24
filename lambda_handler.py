import json
from mcp_server import MCPServer

def lambda_handler(event, context):
    """AWS Lambda handler for MCP Server"""
    
    try:
        body = event.get('body', '')
        request_data = json.loads(body)
        server = MCPServer()
        result = server.handle_request(request_data)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
