-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS hub_dev_db;
CREATE USER IF NOT EXISTS 'hub_dev'@'localhost' IDENTIFIED BY 'hub_dev_pwd';
GRANT ALL PRIVILEGES ON `hub_dev_db`.* TO 'hub_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hub_dev'@'localhost';
FLUSH PRIVILEGES;
