#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e

# Set environment variables for runtime execution
cat <<EOF > /usr/share/nginx/html/config.js
window.APP_CONFIG = {
    SERVER_IP: "${SERVER_IP}",
    SERVER_BACKEND_PORT: "${SERVER_BACKEND_PORT}"
};
EOF

# Start nginx
nginx -g "daemon off;"