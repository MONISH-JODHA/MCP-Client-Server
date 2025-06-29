import json
import schedule
import time
from datetime import datetime
from mcp_client import MCPClient
from typing import Dict, Any, List

class MCPAutomationFramework:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.client = MCPClient(self.config['server_url'])
        self.results = []
    
    def run_cost_analysis(self):
        """Automated cost analysis"""
        result = self.client.get_cost_analysis(self.config.get('cost_analysis_days', 30))
        self._store_result('cost_analysis', result)
        return result
    
    def run_usage_monitoring(self):
        """Automated usage monitoring. Returns a list of results."""
        metrics = self.config.get('usage_metrics', [])
        
        results_list = []
        for metric_config in metrics:
            result = self.client.get_usage_metrics(**metric_config)
            results_list.append(result)
        
        # This operation's result is the list itself.
        self._store_result('usage_monitoring', results_list)
        return results_list # Always return the list of results
    
    def run_service_audit(self):
        """Automated service insights audit"""
        services = self.config.get('audit_services', ['EC2', 'S3', 'RDS'])
        result = self.client.get_service_insights(services)
        self._store_result('service_audit', result)
        return result
    
    def run_ai_analysis(self):
        """Run AI-powered cost optimization analysis"""
        cost_result = self.client.get_cost_analysis(days=7)
        
        if 'result' in cost_result:
            import json
            cost_data = json.dumps(cost_result['result'], indent=2)
            ai_result = self.client.get_ai_analysis(cost_data)
            self._store_result('ai_analysis', ai_result)
            return ai_result
        else:
            error_result = {'error': 'Failed to get cost data for AI analysis', 'details': cost_result.get('error')}
            self._store_result('ai_analysis', error_result)
            return error_result
    
    def _store_result(self, operation: str, result: Any):
        """Store automation results"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'result': result
        }
        self.results.append(entry)
        
        if self.config.get('log_results', True):
            with open(f'mcp_results_{operation}.json', 'w') as f:
                json.dump(entry, f, indent=2)
    
    def schedule_automation(self):
        """Schedule automated tasks"""
        schedule.every().day.at("09:00").do(self.run_cost_analysis)
        schedule.every(4).hours.do(self.run_usage_monitoring)
        schedule.every().week.do(self.run_service_audit)
        
        print("MCP Automation Framework started...")
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def run_once(self) -> Dict[str, Any]:
        """Run all operations once and return a dictionary of their results."""
        results = {
            'cost_analysis': self.run_cost_analysis(),
            'usage_monitoring': self.run_usage_monitoring(),
            'service_audit': self.run_service_audit()
        }
        return results