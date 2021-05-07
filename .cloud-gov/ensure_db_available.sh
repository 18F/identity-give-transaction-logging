#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 CF_SERVICE_NAME SERVICE PLAN

Examples:
  ensure_service_available my-app-db aws-rds micro-psql

NOTE - this script will only create services if they do not exist.
       It will NOT update services to match the provided plan type."
    exit 1
fi

cf_service_name=$1
cf_service=$2
cf_service_plan=$3

# Waits for the cf service status to become create/update succeeded
wait_for_service_creation() {
    time_limit=600 # 10 minutes

    while [ $time_limit -ne 0 ] && [ -z "$service_status" ]; do
        echo "Waiting for service to become available. Seconds before timeout: $time_limit"
        sleep 30
        time_limit=$((time_limit - 30))
        service_status=$(cf service "$cf_service_name" | grep "status:" | grep "create succeeded\|update succeeded")
    done

    # If the service still isn't available, fail the script
    if [ -z "$service_status" ]; then
        echo "Service failed to become ready within the time limit."
        exit 1
    fi

    echo "Service creation finalized"
}

create_service() {
    # Documentation: https://cli.cloudfoundry.org/en-US/v7/create-service.html
    cf create-service "$cf_service" "$cf_service_plan" "$cf_service_name"
}

# Test if cf service exists at all
if ! cf services | grep --silent "^$cf_service_name "; then
    echo "Unable to find service: $cf_service_name. Creating..."
    create_service
    wait_for_service_creation
    exit 0
fi

# The service existed, but the service status is not yet known
echo "Found service $cf_service_name. Checking service status..."

cf_service_status=$(cf service "$cf_service_name" | grep "status:")
success_regex="(create|update) succeeded"

if [[ "$cf_service_status" =~ $success_regex ]]; then
    echo "Service $cf_service_name already available"
elif [[ "$cf_service_status" == *"in progress"* ]]; then
    echo "$cf_service_name creation was 'in progress'."
    wait_for_service_creation
else
    # Status was neither "in progress" or "create|update succeeded". There's likely
    # a problem with the service that can't be resolved without human interaction
    echo "Found cf service: $cf_service_name but status was: $cf_service_status"
    exit 1
fi
