import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, Any, List

class MCPServer:
    def __init__(self, aws_profile: str = None):
        self.session = boto3.Session(profile_name=aws_profile)
        self._ce_client = None
        self._cloudwatch_client = None
        self._bedrock_client = None
        self._service_clients = {}

    @property
    def ce_client(self):
        if not self._ce_client:
            self._ce_client = self.session.client('ce')
        return self._ce_client

    @property
    def cloudwatch(self):
        if not self._cloudwatch_client:
            self._cloudwatch_client = self.session.client('cloudwatch')
        return self._cloudwatch_client

    @property
    def bedrock(self):
        if not self._bedrock_client:
            self._bedrock_client = self.session.client('bedrock-runtime')
        return self._bedrock_client

    def get_service_client(self, service_name: str):
        service_name_lower = service_name.lower()
        if service_name_lower not in self._service_clients:
            self._service_clients[service_name_lower] = self.session.client(service_name_lower)
        return self._service_clients[service_name_lower]
        
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process MCP requests and return metadata"""
        method = request.get('method')
        params = request.get('params', {})
        
        handlers = {
            'get_cost_data': self._get_cost_data,
            'get_usage_metrics': self._get_usage_metrics,
            'get_service_insights': self._get_service_insights,
            'get_ai_analysis': self._get_ai_analysis
        }
        
        if method not in handlers:
            return {'error': f'Unknown method: {method}'}
            
        try:
            return {'result': handlers[method](params)}
        except Exception as e:
            # Added more context to the error
            return {'error': f"An error occurred in method '{method}': {str(e)}"}
    
    def _get_cost_data(self, params: Dict) -> Dict:
        """Retrieve AWS cost data"""
        days = params.get('days', 10)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        return {
            'period': f'{start_date} to {end_date}',
            'cost_data': response['ResultsByTime']
        }
    
    def _get_usage_metrics(self, params: Dict) -> Dict:
        """Get CloudWatch usage metrics"""
        service = params.get('service', 'AWS/EC2')
        metric = params.get('metric', 'CPUUtilization')
        
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace=service,
                MetricName=metric,
                StartTime=datetime.now() - timedelta(hours=24),
                EndTime=datetime.now(),
                Period=3600,
                Statistics=['Average']
            )
            
            # Fix: Convert datetime objects to ISO strings for JSON serialization
            datapoints = response['Datapoints']
            for dp in datapoints:
                if 'Timestamp' in dp:
                    dp['Timestamp'] = dp['Timestamp'].isoformat()

            return {
                'service': service,
                'metric': metric,
                'datapoints': datapoints,
                'count': len(datapoints)
            }
        except Exception as e:
            return {
                'service': service,
                'metric': metric,
                'error': f'No data available: {str(e)}',
                'datapoints': []
            }
        
    def _get_service_insights(self, params: Dict) -> Dict:
        """Get service-level insights"""
        services = params.get('services', ['EC2', 'S3', 'RDS'])
        insights = {}
        
        for service in services:
            try:
                client = self.get_service_client(service)
                if service == 'EC2':
                    instances = client.describe_instances()
                    insights[service] = {
                        'total_instances': len([i for r in instances['Reservations'] for i in r['Instances']]),
                        'running_instances': len([i for r in instances['Reservations'] for i in r['Instances'] if i['State']['Name'] == 'running'])
                    }
                elif service == 'S3':
                    buckets = client.list_buckets()
                    insights[service] = {'bucket_count': len(buckets['Buckets'])}
            except Exception as e:
                insights[service] = {'error': str(e)}
        
        return insights
    
    def _get_ai_analysis(self, params: Dict) -> Dict:
        """Get AI-powered cost optimization insights"""
        data = params.get('data', '')
        
        response = self.bedrock.invoke_model(
            modelId='amazon.titan-text-premier-v1:0',
            body=json.dumps({
                'inputText': f'Analyze this AWS cost/usage data and provide optimization recommendations: {data}',
                'textGenerationConfig': {
                    'maxTokenCount': 500,
                    'temperature': 0.7
                }
            }),
            contentType="application/json",
            accept="application/json"
        )
        
        result = json.loads(response['body'].read())
        # Fix: Correctly parse the response for the Titan model
        return {'analysis': result['results'][0]['outputText']}