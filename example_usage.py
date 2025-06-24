#!/usr/bin/env python3
from mcp_server import MCPServer
import json

def test_local():
    """Test MCP Server locally without Lambda"""
    server = MCPServer()
    
    # Test cost data
    cost_result = server.handle_request({
        'method': 'get_cost_data',
        'params': {'days': 7}
    })
    
    # Test usage metrics
    usage_result = server.handle_request({
        'method': 'get_usage_metrics',
        'params': {'service': 'AWS/EC2', 'metric': 'CPUUtilization'}
    })
    
    # Test service insights
    service_result = server.handle_request({
        'method': 'get_service_insights',
        'params': {'services': ['EC2', 'S3']}
    })
    
    results = {
        'cost_analysis': cost_result,
        'usage_monitoring': usage_result,
        'service_audit': service_result
    }
    
    print("MCP Local Test Results:")
    for operation, result in results.items():
        print(f"\n{operation.upper()}:")
        print(f"Status: {'Success' if 'result' in result else 'Error'}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        elif 'result' in result:
            print(f"Data: {type(result['result']).__name__} with {len(str(result['result']))} chars")

if __name__ == "__main__":
    test_local()
