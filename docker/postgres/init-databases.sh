#!/bin/sh
set -e

for db in auth_service audit_service user_service category_service product_service restaurant_service table_service order_service; do
  if ! psql -h postgres -U postgres -d facilcomanda -tAc "SELECT 1 FROM pg_database WHERE datname = '$db'" | grep -q 1; then
    psql -h postgres -U postgres -d facilcomanda -c "CREATE DATABASE \"$db\""
  fi
done
