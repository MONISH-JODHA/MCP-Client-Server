#!/usr/bin/env python3
from automation_framework import MCPAutomationFramework

def main():
    framework = MCPAutomationFramework('config.json')
    results = framework.run_once()
    
    print("MCP Lambda Test Results:")
    for operation, result in results.items():
        print(f"\n{operation.upper()}:")
        print(f"Status: {'Success' if 'result' in result else 'Error'}")
        if 'error' in result:
            print(f"Error: {result['error']}")
        if 'result' in result:
            print(f"Success: Data received")

if __name__ == "__main__":
    main()
