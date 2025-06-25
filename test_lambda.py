#!/usr/bin/env python3
from automation_framework import MCPAutomationFramework
import json

def main():
    framework = MCPAutomationFramework('config.json')
    results = framework.run_once()
    
    print("MCP Lambda Test Results:")
    
    for operation, result in results.items():
        print(f"\n{operation.upper()}:")
        
        # Special handling for usage_monitoring, which returns a list
        if operation == 'usage_monitoring':
            if isinstance(result, list):
                print(f"Status: Partial or Full Success (received {len(result)} results)")
                for i, res in enumerate(result):
                    if 'error' in res:
                        service = res.get('service', 'Unknown')
                        metric = res.get('metric', 'Unknown')
                        print(f"  - Result {i+1} for {service}/{metric}: Error - {res['error']}")
                    else:
                        service = res.get('service', 'Unknown')
                        metric = res.get('metric', 'Unknown')
                        print(f"  - Result {i+1} for {service}/{metric}: Success - {res.get('count', 0)} datapoints found")
            else:
                # Fallback for unexpected format
                print(f"Status: Error")
                print(f"  - Details: {result.get('error', 'Unknown error')}")

        # Standard handling for other operations
        else:
            if 'result' in result:
                print(f"Status: Success")
                print(f"  - Success: Data received")
            elif 'error' in result:
                print(f"Status: Error")
                print(f"  - Error: {result['error']}")

if __name__ == "__main__":
    main()
    
