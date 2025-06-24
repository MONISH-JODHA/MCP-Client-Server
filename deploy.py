import boto3
import zipfile
import os

def deploy_lambda():
    lambda_client = boto3.client('lambda')
    
    # Create deployment package
    with zipfile.ZipFile('mcp-server.zip', 'w') as z:
        z.write('lambda_handler.py', 'lambda_handler.py')
        z.write('mcp_server.py')
    
    # Create/update Lambda function
    try:
        with open('mcp-server.zip', 'rb') as f:
            lambda_client.create_function(
                FunctionName='mcp-server',
                Runtime='python3.10',
                Role='arn:aws:iam::411335221056:role/mcp-lambda-role',
                Handler='lambda_handler.lambda_handler',
                Code={'ZipFile': f.read()},
                Timeout=30
            )
    except lambda_client.exceptions.ResourceConflictException:
        with open('mcp-server.zip', 'rb') as f:
            lambda_client.update_function_code(
                FunctionName='mcp-server',
                ZipFile=f.read()
            )
    
    # Create Function URL
    try:
        response = lambda_client.create_function_url_config(
            FunctionName='mcp-server',
            AuthType='NONE'
        )
        print(f"Lambda URL: {response['FunctionUrl']}")
        return response['FunctionUrl']
    except lambda_client.exceptions.ResourceConflictException:
        response = lambda_client.get_function_url_config(FunctionName='mcp-server')
        print(f"Existing Lambda URL: {response['FunctionUrl']}")
        return response['FunctionUrl']

if __name__ == "__main__":
    url = deploy_lambda()
    print(f"Use this URL in config.json: {url}")
