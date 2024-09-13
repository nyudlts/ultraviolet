# check-services.sh
#!/bin/bash

# Function to check service status
check_services() {
  echo "Checking services status..."
  status=$(invenio-cli services status)
  echo "$status"

  if [[ "$status" == *"redis: up and running."* && "$status" == *"postgresql: up and running."* && "$status" == *"search: up and running."* ]]; then
    echo "All services are up and running."
    return 0
  else
    echo "Some services are not ready yet."
    return 1
  fi
}

# Loop until all services are up
until check_services; do
  echo "Waiting for all services to be fully operational..."
  sleep 10 # wait for 10s
done
