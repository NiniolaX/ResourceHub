-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS hub_test_db;
CREATE USER IF NOT EXISTS 'hub_test'@'localhost' IDENTIFIED BY 'hub_test_pwd';
GRANT ALL PRIVILEGES ON `hub_test_db`.* TO 'hub_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hub_test'@'localhost';
FLUSH PRIVILEGES;
