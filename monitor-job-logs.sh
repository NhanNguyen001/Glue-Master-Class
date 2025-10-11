#!/bin/bash

# Monitor EKS job logs with fallback options
# Usage: ./monitor-job-logs.sh <job-name> [namespace]

JOB_NAME=${1:-"account-producer"}
NAMESPACE=${2:-"dataloader"}

echo "🔍 Monitoring logs for job: $JOB_NAME in namespace: $NAMESPACE"
echo "=================================================="

# Function to check if pods exist
check_pods() {
    kubectl get pods -n $NAMESPACE -l job-name=$JOB_NAME --no-headers 2>/dev/null | wc -l
}

# Function to get pod status
get_pod_status() {
    kubectl get pods -n $NAMESPACE -l job-name=$JOB_NAME -o wide 2>/dev/null
}

# Function to get job details
get_job_details() {
    echo "📋 Job Details:"
    kubectl describe job $JOB_NAME -n $NAMESPACE 2>/dev/null || echo "❌ Job not found or accessible"
    echo ""
}

# Function to get recent events
get_recent_events() {
    echo "📅 Recent Events (last 1 hour):"
    kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' \
        --field-selector involvedObject.name=$JOB_NAME \
        --output='custom-columns=TIME:.lastTimestamp,TYPE:.type,REASON:.reason,MESSAGE:.message' \
        2>/dev/null || echo "❌ No events found"
    echo ""
}

# Function to get logs with timeout
get_logs_with_timeout() {
    echo "📄 Attempting to get logs..."
    
    # Try with timeout
    timeout 10 kubectl logs job/$JOB_NAME -n $NAMESPACE --timestamps=true 2>/dev/null
    
    if [ $? -eq 124 ]; then
        echo "⏰ Timeout occurred - pods might be cleaned up"
        return 1
    elif [ $? -ne 0 ]; then
        echo "❌ Error getting logs"
        return 1
    fi
    return 0
}

# Function to suggest alternatives
suggest_alternatives() {
    echo "💡 Alternative monitoring options:"
    echo ""
    echo "1. Monitor new job executions:"
    echo "   kubectl get jobs -n $NAMESPACE -w"
    echo ""
    echo "2. Check CloudWatch logs (if Container Insights enabled):"
    echo "   aws logs describe-log-groups --log-group-name-prefix '/aws/containerinsights/gft-dm-data-migration'"
    echo ""
    echo "3. Monitor Step Function executions:"
    echo "   aws stepfunctions list-executions --state-machine-arn <your-state-machine-arn>"
    echo ""
    echo "4. Set up log forwarding for future jobs:"
    echo "   - Enable Container Insights on EKS cluster"
    echo "   - Configure Fluent Bit or CloudWatch agent"
    echo ""
}

# Main execution
echo "🔄 Checking job status..."
get_job_details

POD_COUNT=$(check_pods)
echo "📦 Found $POD_COUNT pod(s) for job $JOB_NAME"

if [ $POD_COUNT -gt 0 ]; then
    echo ""
    echo "🏃 Pod Status:"
    get_pod_status
    echo ""
    
    if ! get_logs_with_timeout; then
        echo ""
        get_recent_events
        suggest_alternatives
    fi
else
    echo "❌ No pods found for job $JOB_NAME"
    echo "   This usually means the job completed and pods were garbage collected."
    echo ""
    get_recent_events
    suggest_alternatives
fi

echo ""
echo "✅ Monitoring complete" 