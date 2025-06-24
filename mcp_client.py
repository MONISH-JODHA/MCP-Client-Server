import json
import requests
from typing import Dict, Any

class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
    
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send MCP request"""
        request_data = {
            'method': method,
            'params': params or {}
        }
        
        payload = json.dumps(request_data)
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.server_url,
                data=payload,
                headers=headers,
                timeout=30
            )
            if response.status_code != 200:
                return {'error': f'HTTP {response.status_code}: {response.text}'}
            return response.json()
        except Exception as e:
            return {'error': f'Request failed: {str(e)}'}
    
    def get_cost_analysis(self, days: int = 30) -> Dict[str, Any]:
        """Get cost analysis from AWS"""
        return self.send_request('get_cost_data', {'days': days})
    
    def get_usage_metrics(self, service: str = 'AWS/EC2', metric: str = 'CPUUtilization') -> Dict[str, Any]:
        """Get usage metrics"""
        return self.send_request('get_usage_metrics', {'service': service, 'metric': metric})
    
    def get_service_insights(self, services: list = None) -> Dict[str, Any]:
        """Get service-level insights"""
        return self.send_request('get_service_insights', {'services': services or ['EC2', 'S3', 'RDS']})
    
    def get_ai_analysis(self, data: str) -> Dict[str, Any]:
        """Get AI-powered cost optimization analysis"""
        return self.send_request('get_ai_analysis', {'data': data})
