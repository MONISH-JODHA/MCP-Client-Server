# MCP Automation Framework

An automation framework using the MCP (Model Context Protocol) to streamline secure data exchange between MCP Server API and MCP Client for AWS cloud metadata retrieval and processing.

## Overview

This framework enables automated retrieval and processing of cloud metadata including cost, usage, and service-level insights from AWS accounts through a secure, authenticated request-response model.

## Architecture

```
MCP Client → API Gateway → Lambda Function (MCP Server) → AWS Services
```

- **MCP Client**: Sends authenticated requests for AWS metadata
- **API Gateway**: Routes requests to Lambda with proper authentication
- **MCP Server**: Processes requests and queries AWS services
- **AWS Services**: Cost Explorer, CloudWatch, EC2, S3, RDS for metadata

## Core Files

### 1. MCP Server (`mcp_server.py`)
**Purpose**: Core server that handles AWS metadata queries

**Key Features**:
- Processes MCP requests using method-based routing
- Integrates with AWS Cost Explorer for cost analysis
- Retrieves CloudWatch metrics for usage monitoring
- Collects service insights from EC2, S3, RDS
- Includes AI-powered analysis using Bedrock Claude 3 Haiku

**Methods**:
- `get_cost_data`: Retrieves AWS cost data over specified time periods
- `get_usage_metrics`: Gets CloudWatch usage metrics for services
- `get_service_insights`: Collects service-level information and counts
- `get_ai_analysis`: Provides AI-powered cost optimization recommendations

### 2. MCP Client (`mcp_client.py`)
**Purpose**: Simple client for sending requests to MCP Server via API Gateway

**Key Features**:
- Clean HTTP request handling with error reporting
- Simplified constructor (only requires server URL)
- Convenience methods for common operations
- No authentication needed (handled by API Gateway)

**Methods**:
- `send_request`: Core method for API calls
- `get_cost_analysis`: Wrapper for cost data retrieval
- `get_usage_metrics`: Wrapper for usage metrics
- `get_service_insights`: Wrapper for service insights

### 3. Automation Framework (`automation_framework.py`)
**Purpose**: Orchestrates scheduled automation tasks

**Key Features**:
- Configurable scheduling using the `schedule` library
- Result storage and logging
- Batch operations for multiple metrics
- One-time execution for testing

**Operations**:
- `run_cost_analysis`: Daily cost analysis automation
- `run_usage_monitoring`: Periodic usage metrics collection
- `run_service_audit`: Weekly service insights audit
- `schedule_automation`: Continuous scheduled execution

### 4. Lambda Handler (`lambda_handler_simple.py`)
**Purpose**: AWS Lambda entry point for serverless MCP Server deployment

**Key Features**:
- Simplified handler without authentication (handled by API Gateway)
- JSON request/response processing
- Error handling and HTTP status codes
- Integration with MCP Server class

## Configuration Files
# MCP Automation Framework

An automation framework using the MCP (Model Context Protocol) to streamline secure data exchange between MCP Server API and MCP Client for AWS cloud metadata retrieval and processing.

## Overview

This framework enables automated retrieval and processing of cloud metadata including cost, usage, and service-level insights from AWS accounts through a secure, authenticated request-response model.

## Architecture

```
MCP Client → API Gateway → Lambda Function (MCP Server) → AWS Services
```

- **MCP Client**: Sends authenticated requests for AWS metadata
- **API Gateway**: Routes requests to Lambda with proper authentication
- **MCP Server**: Processes requests and queries AWS services
- **AWS Services**: Cost Explorer, CloudWatch, EC2, S3, RDS for metadata

## Core Files

### 1. MCP Server (`mcp_server.py`)
**Purpose**: Core server that handles AWS metadata queries

**Key Features**:
- Processes MCP requests using method-based routing
- Integrates with AWS Cost Explorer for cost analysis
- Retrieves CloudWatch metrics for usage monitoring
- Collects service insights from EC2, S3, RDS
- Includes AI-powered analysis using Bedrock Claude 3 Haiku

**Methods**:
- `get_cost_data`: Retrieves AWS cost data over specified time periods
- `get_usage_metrics`: Gets CloudWatch usage metrics for services
- `get_service_insights`: Collects service-level information and counts
- `get_ai_analysis`: Provides AI-powered cost optimization recommendations

### 2. MCP Client (`mcp_client.py`)
**Purpose**: Simple client for sending requests to MCP Server via API Gateway

**Key Features**:
- Clean HTTP request handling with error reporting
- Simplified constructor (only requires server URL)
- Convenience methods for common operations
- No authentication needed (handled by API Gateway)

**Methods**:
- `send_request`: Core method for API calls
- `get_cost_analysis`: Wrapper for cost data retrieval
- `get_usage_metrics`: Wrapper for usage metrics
- `get_service_insights`: Wrapper for service insights

### 3. Automation Framework (`automation_framework.py`)
**Purpose**: Orchestrates scheduled automation tasks

**Key Features**:
- Configurable scheduling using the `schedule` library
- Result storage and logging
- Batch operations for multiple metrics
- One-time execution for testing

**Operations**:
- `run_cost_analysis`: Daily cost analysis automation
- `run_usage_monitoring`: Periodic usage metrics collection
- `run_service_audit`: Weekly service insights audit
- `schedule_automation`: Continuous scheduled execution

### 4. Lambda Handler (`lambda_handler_simple.py`)
**Purpose**: AWS Lambda entry point for serverless MCP Server deployment

**Key Features**:
- Simplified handler without authentication (handled by API Gateway)
- JSON request/response processing
- Error handling and HTTP status codes
- Integration with MCP Server class






MCP Server with Amazon Bedrock

The MCP Server is an AWS Lambda function that handles AWS-related tasks like checking costs or monitoring usage. It gathers data from AWS services such as Cost Explorer, CloudWatch, EC2, and IAM. Then, it sends this data as a prompt to Amazon Bedrock, using models like Claude 3 Haiku or Titan Text, to get helpful AI-generated insights. The server is designed to retry if something fails, manage traffic limits, and runs without storing any data permanently.

Example Bedrock call:

response = bedrock_runtime.invoke_model(
body=json.dumps(payload),
modelId="amazon.titan-text-premier-v1:0",
contentType="application/json",
accept="application/json"
)

Cost Overview

Amazon Bedrock charges based on the number of input and output tokens. For Titan Text Premier, it's $0.0005 for 1,000 input tokens and $0.0015 for 1,000 output tokens.

API Gateway only charges when you use it. You also get 1 million free API calls each month for the first 12 months.

AWS Lambda charges based on how often your function runs, how long it runs, and how much memory it uses. You can use the AWS calculator to estimate costs.

Security Highlights

API Gateway controls how requests are handled and limits traffic.

Lambda functions use only the permissions they need. Environment variables can be encrypted. Running in a VPC helps keep resources private. Access to the Lambda function is restricted with policies. Logging is turned on for monitoring.

Since it's serverless, there are no always-on servers or open network ports. Everything is tracked and monitored using CloudWatch.

MCP Client Options

Amazon Q Developer is the only built-in MCP client.

Other AWS services like Lambda, ECS/Fargate, Step Functions, and EventBridge can also work as MCP clients but need to be set up manually.

For development, using Lambda is easiest. For production, ECS/Fargate with API Gateway is recommended.

