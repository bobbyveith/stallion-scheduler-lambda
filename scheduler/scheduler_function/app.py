import json
import logging
import requests

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Scheduler function that runs at 6am EST daily
    
    Parameters
    ----------
    event: dict, required
        EventBridge scheduled event
        
    context: object, required
        Lambda Context runtime methods and attributes
        
    Returns
    ------
    dict: Response containing execution details
    """
    logger.info("Scheduler function executing")
    
    # API endpoint
    api_url = "https://api.stallion-wholesale.com/api/v1/scheduler/tasks/run"
    
    # Request payload
    payload = {
        "task_name": "Run Shipstation"
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request with a 5 second timeout
        # We just need to send the request successfully, not wait for a full response
        response = requests.post(api_url, json=payload, headers=headers, timeout=5)
        
        # If we get here without an exception, consider it a success
        logger.info(f"API request sent successfully. Status code: {response.status_code}")
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Scheduler function executed successfully",
                "info": "Request sent to API",
                "timestamp": event.get("time", "unknown")
            }),
        }
    except requests.exceptions.Timeout:
        # This is actually expected behavior, so we treat it as success
        logger.info("API request timed out, which is expected behavior. Task is likely running.")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Scheduler function executed successfully",
                "info": "Request timed out as expected, task is likely running",
                "timestamp": event.get("time", "unknown")
            }),
        }
    except requests.exceptions.RequestException as e:
        # Log the error - these are real failures
        logger.error(f"API call failed: {str(e)}")
        
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Scheduler function failed",
                "error": str(e),
                "timestamp": event.get("time", "unknown")
            }),
        } 