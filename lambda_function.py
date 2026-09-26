import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")


def is_auto_stop_enabled(tags):
    """Return True when the EC2 instance has AutoStop=true."""
    for tag in tags or []:
        key = str(tag.get("Key", "")).strip()
        value = str(tag.get("Value", "")).strip().lower()
        if key.lower() == "autostop" and value == "true":
            return True
    return False


def lambda_handler(event, context):
    logger.info("Starting EC2 Cost Optimizer")

    stopped_instances = []
    next_token = None

    while True:
        params = {}
        if next_token:
            params["NextToken"] = next_token

        response = ec2.describe_instances(**params)

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance["InstanceId"]
                state = instance["State"]["Name"]
                tags = instance.get("Tags", [])
                auto_stop = is_auto_stop_enabled(tags)

                logger.info(
                    "Instance: %s, State: %s, AutoStop: %s",
                    instance_id,
                    state,
                    auto_stop,
                )

                if auto_stop and state == "running":
                    logger.info("Stopping approved instance: %s", instance_id)
                    ec2.stop_instances(InstanceIds=[instance_id])
                    stopped_instances.append(instance_id)
                else:
                    logger.info("Skipping instance: %s", instance_id)

        next_token = response.get("NextToken")
        if not next_token:
            break

    logger.info("Stopped instances: %s", stopped_instances)

    return {
        "statusCode": 200,
        "stopped_instances": stopped_instances,
    }