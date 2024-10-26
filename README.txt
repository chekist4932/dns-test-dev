1. cd sql-scripts

2. psql -h 172.18.0.2 -U dns-test-dev-usr -d dns-test-dev -f test_data_city.sql && \
psql -h 172.18.0.2 -U dns-test-dev-usr -d dns-test-dev -f test_data_store.sql && \
psql -h 172.18.0.2 -U dns-test-dev-usr -d dns-test-dev -f test_data_product.sql && \
psql -h 172.18.0.2 -U dns-test-dev-usr -d dns-test-dev -f test_data_sale.sql 

3. docker-compose up -d --build
