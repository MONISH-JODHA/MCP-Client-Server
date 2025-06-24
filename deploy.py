import boto3
import zipfile
import time

def deploy_lambda():
    lambda_client = boto3.client('lambda')
    function_name = 'mcp-server'
    handler_name = 'lambda_handler.lambda_handler'
    role_arn = 'arn:aws:iam::411335221056:role/mcp-lambda-role'
    runtime = 'python3.10'

    # Create deployment package
    zip_file_name = 'mcp-server.zip'
    with zipfile.ZipFile(zip_file_name, 'w') as z:
        z.write('lambda_handler.py')
        z.write('mcp_server.py')
    
    with open(zip_file_name, 'rb') as f:
        zip_bytes = f.read()

    # Create or update Lambda function
    try:
        lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler_name,
            Code={'ZipFile': zip_bytes},
            Timeout=30,
            MemorySize=256
        )
        print(f"Created Lambda function: {function_name}")
    except lambda_client.exceptions.ResourceConflictException:
        print("Function already exists. Updating code and configuration...")
        
        # --- THE FIX IS HERE ---
        # 1. Update the code
        print("1/3: Updating function code...")
        lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_bytes
        )
        
        # 2. Use a "waiter" to pause until the update is complete
        print("2/3: Waiting for the function code update to complete...")
        waiter = lambda_client.get_waiter('function_updated')
        waiter.wait(
            FunctionName=function_name,
            WaiterConfig={'Delay': 5, 'MaxAttempts': 20} # Poll every 5 seconds
        )
        print("     Update complete.")

        # 3. Now that the function is stable, update the configuration
        print("3/3: Updating function configuration...")
        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Handler=handler_name,
            Role=role_arn,
            Timeout=30,
            MemorySize=256
        )
        print("     Configuration updated.")
        # --- END OF FIX ---

if __name__ == "__main__":
    deploy_lambda()
    print("\nDeployment complete. The script now waits for updates to finish.")