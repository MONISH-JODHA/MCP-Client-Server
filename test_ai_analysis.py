#!/usr/bin/env python3
from mcp_client import MCPClient
import json

def test_ai_analysis():
    client = MCPClient("https://d7g1azx6ag.execute-api.us-east-1.amazonaws.com/dev")
    
    # Get cost data first
    cost_result = client.get_cost_analysis(days=7)
    
    if 'result' in cost_result:
        # Convert cost data to string for AI analysis
        cost_data = json.dumps(cost_result['result'], indent=2)
        
        # Get AI analysis
        ai_result = client.get_ai_analysis(cost_data)
        
        print("AI Cost Optimization Analysis:")
        if 'result' in ai_result:
            print(ai_result['result']['analysis'])
        else:
            print(f"Error: {ai_result.get('error', 'Unknown error')}")
    else:
        print(f"Failed to get cost data: {cost_result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_ai_analysis()