#!/bin/bash

echo "CREATE ROLE dekker_lab WITH LOGIN PASSWORD 'CHYYTS14#';" | sudo -u postgres psql
echo "CREATE ROLE nanda WITH LOGIN PASSWORD 'CHYYTS14#';" | sudo -u postgres psql
echo "create database clims_db;" |  sudo -u postgres psql
echo "GRANT ALL PRIVILEGES ON DATABASE clims_db TO dekker_lab;" | sudo -u postgres psql
echo "GRANT ALL PRIVILEGES ON DATABASE clims_db TO nanda;" | sudo -u postgres psql
echo "ALTER ROLE dekker_lab SET client_encoding TO 'utf8';" | sudo -u postgres psql
echo "ALTER ROLE dekker_lab SET default_transaction_isolation TO 'read committed';" | sudo -u postgres psql
