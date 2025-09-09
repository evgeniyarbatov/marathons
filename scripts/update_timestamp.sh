#!/bin/bash

# Update the last deploy timestamp in App.vue
APP_VUE_FILE="site/src/App.vue"
CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Replace the timestamp in App.vue
sed -i "s/const lastDeployTime = new Date('.*');/const lastDeployTime = new Date('${CURRENT_TIMESTAMP}');/" "${APP_VUE_FILE}"

echo "Updated timestamp to: ${CURRENT_TIMESTAMP}"