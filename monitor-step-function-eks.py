#!/usr/bin/env python3
"""
Monitor Step Function executions and corresponding EKS jobs
"""

import boto3
import subprocess
import json
import time
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StepFunctionEKSMonitor:
    def __init__(self, step_function_arn, cluster_name, namespace="dataloader"):
        self.step_function_arn = step_function_arn
        self.cluster_name = cluster_name
        self.namespace = namespace
        self.stepfunctions_client = boto3.client('stepfunctions', region_name='ap-southeast-1')
        
    def get_recent_executions(self, hours=24):
        """Get Step Function executions from the last N hours"""
        try:
            response = self.stepfunctions_client.list_executions(
                stateMachineArn=self.step_function_arn,
                maxResults=50
            )
            
            recent_executions = []
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            for execution in response['executions']:
                start_date = execution['startDate'].replace(tzinfo=None)
                if start_date > cutoff_time:
                    recent_executions.append(execution)
                    
            return recent_executions
        except Exception as e:
            logger.error(f"Error getting Step Function executions: {e}")
            return []
    
    def get_execution_details(self, execution_arn):
        """Get detailed information about a specific execution"""
        try:
            response = self.stepfunctions_client.describe_execution(
                executionArn=execution_arn
            )
            return response
        except Exception as e:
            logger.error(f"Error getting execution details: {e}")
            return None
    
    def get_eks_jobs(self):
        """Get current EKS jobs in the namespace"""
        try:
            cmd = f"kubectl get jobs -n {self.namespace} -o json"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                jobs_data = json.loads(result.stdout)
                return jobs_data.get('items', [])
            else:
                logger.error(f"Error getting EKS jobs: {result.stderr}")
                return []
        except Exception as e:
            logger.error(f"Error running kubectl command: {e}")
            return []
    
    def get_job_logs(self, job_name):
        """Get logs for a specific job"""
        try:
            cmd = f"kubectl logs job/{job_name} -n {self.namespace} --tail=20"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error getting logs: {result.stderr}"
        except Exception as e:
            return f"Error running kubectl logs: {e}"
    
    def monitor_active_executions(self):
        """Monitor currently active Step Function executions and corresponding EKS jobs"""
        logger.info("Starting monitoring...")
        
        while True:
            try:
                # Get recent executions
                executions = self.get_recent_executions(hours=2)
                running_executions = [e for e in executions if e['status'] == 'RUNNING']
                
                logger.info(f"Found {len(running_executions)} running executions")
                
                # Get current EKS jobs
                eks_jobs = self.get_eks_jobs()
                account_producer_jobs = [
                    job for job in eks_jobs 
                    if 'account-producer' in job['metadata']['name']
                ]
                
                logger.info(f"Found {len(account_producer_jobs)} account-producer jobs in EKS")
                
                # Display current status
                print("\n" + "="*80)
                print(f"MONITORING REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*80)
                
                print(f"\n📊 STEP FUNCTION EXECUTIONS (Running):")
                for execution in running_executions:
                    status_details = self.get_execution_details(execution['executionArn'])
                    print(f"  ▶️  {execution['name']}")
                    print(f"     Status: {execution['status']}")
                    print(f"     Started: {execution['startDate']}")
                    if status_details and 'input' in status_details:
                        input_data = json.loads(status_details['input'])
                        if 'type' in input_data:
                            print(f"     Job Type: {input_data['type']}")
                
                print(f"\n🚀 EKS JOBS (account-producer):")
                for job in account_producer_jobs:
                    job_name = job['metadata']['name']
                    creation_time = job['metadata']['creationTimestamp']
                    
                    # Get job status
                    status = job.get('status', {})
                    conditions = status.get('conditions', [])
                    
                    print(f"  🔧 {job_name}")
                    print(f"     Created: {creation_time}")
                    print(f"     Active: {status.get('active', 0)}")
                    print(f"     Succeeded: {status.get('succeeded', 0)}")
                    print(f"     Failed: {status.get('failed', 0)}")
                    
                    if conditions:
                        latest_condition = conditions[-1]
                        print(f"     Latest Status: {latest_condition.get('type')} - {latest_condition.get('status')}")
                
                print("\n" + "="*80)
                
                # Wait before next check
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)

def main():
    # Configuration - Update these values for your environment
    STEP_FUNCTION_ARN = "arn:aws:states:ap-southeast-1:YOUR_ACCOUNT_ID:stateMachine:YOUR_STATE_MACHINE_NAME"
    CLUSTER_NAME = "gft-dm-data-migration"
    NAMESPACE = "dataloader"
    
    print("Step Function EKS Job Monitor")
    print("=" * 40)
    print(f"Cluster: {CLUSTER_NAME}")
    print(f"Namespace: {NAMESPACE}")
    print("Press Ctrl+C to stop monitoring\n")
    
    monitor = StepFunctionEKSMonitor(STEP_FUNCTION_ARN, CLUSTER_NAME, NAMESPACE)
    monitor.monitor_active_executions()

if __name__ == "__main__":
    main() 