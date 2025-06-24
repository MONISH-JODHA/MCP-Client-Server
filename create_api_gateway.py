import boto3
import json

def create_api_gateway():
    apigateway = boto3.client('apigateway')
    lambda_client = boto3.client('lambda')
    
    # Create API Gateway
    api = apigateway.create_rest_api(
        name='mcp-api',
        description='MCP Server API'
    )
    api_id = api['id']
    
    # Get root resource
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = resources['items'][0]['id']
    
    # Create POST method
    apigateway.put_method(
        restApiId=api_id,
        resourceId=root_id,
        httpMethod='POST',
        authorizationType='NONE'
    )
    
    # Set integration
    lambda_arn = f'arn:aws:lambda:us-east-1:411335221056:function:mcp-server'
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=root_id,
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    
    # Deploy API
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='dev'
    )
    
    # # Add Lambda permission
    # lambda_client.add_permission(
    #     FunctionName='mcp-server',
    #     StatementId='api-gateway-invoke',
    #     Action='lambda:InvokeFunction',
    #     Principal='apigateway.amazonaws.com',
    #     SourceArn=f'arn:aws:execute-api:us-east-1:411335221056:{api_id}/*/*'
    # )
    
    api_url = f'https://{api_id}.execute-api.us-east-1.amazonaws.com/dev'
    print(f"API Gateway URL: {api_url}")
    
    # Update config
    with open('config.json', 'r') as f:
        config = json.load(f)
    config['server_url'] = api_url
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    return api_url

if __name__ == "__main__":
    create_api_gateway()
