#!/bin/bash

# Update the last deploy timestamp by writing to public file
LAST_UPDATE_FILE="site/public/last_update.txt"
CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Write timestamp to public file
echo "${CURRENT_TIMESTAMP}" > "${LAST_UPDATE_FILE}"

echo "Updated timestamp to: ${CURRENT_TIMESTAMP}"