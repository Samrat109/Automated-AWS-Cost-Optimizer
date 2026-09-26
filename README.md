# Automated AWS Cost Optimizer

This project automatically stops EC2 instances that are tagged with `AutoStop=true`, helping reduce unnecessary compute costs during idle or off-hours periods.

## What it does

The AWS Lambda function:

- Lists all EC2 instances in the current account/region
- Checks each instance for the `AutoStop` tag
- Stops any instance whose tag value is exactly `true`
- Skips instances that are already stopped or not tagged for auto-stop
- Logs all actions for auditing and troubleshooting

## Architecture

- AWS Lambda runs the optimizer logic
- Amazon EC2 provides the target compute resources
- Amazon EventBridge can trigger the Lambda on a schedule
- IAM permissions allow DescribeInstances and StopInstances actions

## Example instance tag

Add this tag to any EC2 instance you want the optimizer to stop automatically:

- Key: `AutoStop`
- Value: `true`

## Deployment

### Prerequisites

- AWS CLI configured with valid credentials
- AWS SAM CLI installed
- Python 3.12 or compatible runtime

### Package and deploy

```bash
sam build
sam deploy --guided
```

When prompted, set the stack name, AWS region, and confirm the changes. The template creates the Lambda function and the scheduled trigger.

## Schedule configuration

The default schedule is configured in `template.yaml` using a cron expression. You can change it to match your business hours or maintenance windows.

Example:

```yaml
Schedule: cron(0 18 ? * MON-FRI *)
```

This example runs at 6:00 PM UTC Monday through Friday.

## Local validation

You can run a quick syntax check for the Lambda code:

```bash
python -m py_compile lambda_function.py
```

## Files

- `lambda_function.py` – Lambda entry point and optimization logic
- `template.yaml` – SAM deployment template
- `requirements.txt` – Python dependencies

## Notes

- The function only stops instances that explicitly opt in with the `AutoStop=true` tag.
- It is designed as a cost-saving automation and should be reviewed carefully before broad production use.
- For production workloads, validate the schedule against business requirements and maintenance windows.
