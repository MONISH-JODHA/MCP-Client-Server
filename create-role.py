import boto3
import json

def create_lambda_role():
    iam = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    # Create role
    try:
        iam.create_role(
            RoleName='mcp-lambda-role',
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
    except iam.exceptions.EntityAlreadyExistsException:
        pass
    
    # Attach policy
    with open('lambda-policy.json', 'r') as f:
        policy = f.read()
    
    try:
        iam.put_role_policy(
            RoleName='mcp-lambda-role',
            PolicyName='mcp-lambda-policy',
            PolicyDocument=policy
        )
    except Exception as e:
        print(f"Policy attachment failed: {e}")
    
    # Get role ARN
    role = iam.get_role(RoleName='mcp-lambda-role')
    print(f"Role ARN: {role['Role']['Arn']}")
    return role['Role']['Arn']

if __name__ == "__main__":
    create_lambda_role()