#!/bin/sh

set -e

echo "$JWT_PRIVATE_KEY" > /app/src/certs/jwt/private.pem
echo "$JWT_PUBLIC_KEY" > /app/src/certs/jwt/public.pem
chmod 600 /app/src/certs/jwt/*.pem

exec "$@"