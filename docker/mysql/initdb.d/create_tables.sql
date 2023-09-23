CREATE DATABASE IF NOT EXISTS alice;
USE alice_services;


# Tables
CREATE TABLE IF NOT EXISTS customer
(
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name            VARCHAR(50) DEFAULT 'Customer',
    nickname        VARCHAR(10),
    email           VARCHAR(100),
    customer_status ENUM ('valid', 'invalid'),
    customer_type   ENUM ('academic', 'consumer', 'commercial', 'enterprise', 'partner', 'internal'),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS services
(
    id                      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name                    VARCHAR(100) DEFAULT 'construction name',
    construction_alias_name VARCHAR(10),
    price                   INT UNSIGNED,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS construction
(
    id                  INT UNSIGNED NOT NULL AUTO_INCREMENT,
    customer            INT UNSIGNED,
    services            INT UNSIGNED,
    construction_status ENUM ('trial', 'valid', 'invalid'),
    PRIMARY KEY (id),
    FOREIGN KEY (customer) REFERENCES customer (id),
    FOREIGN KEY (services) REFERENCES services (id)
);

CREATE TABLE IF NOT EXISTS node
(
    id                INT UNSIGNED NOT NULL AUTO_INCREMENT,
    node_name         VARCHAR(100),
    registration_code VARCHAR(72),
    customer          INT UNSIGNED,
    PRIMARY KEY (id),
    FOREIGN KEY (customer) REFERENCES customer (id)
);

CREATE TABLE IF NOT EXISTS data
(
    id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
    node          INT UNSIGNED,
    data_type     VARCHAR(100),
    data_category VARCHAR(100),
    data_value    DOUBLE(30, 5),
    daq_datetime  DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY (node) REFERENCES node (id)
);

CREATE TABLE IF NOT EXISTS node_settings
(
    id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
    node             INT UNSIGNED,
    setting_category VARCHAR(100),
    setting_value    VARCHAR(10),
    setting_datetime DATETIME,
    setting_valid    BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (node) REFERENCES node (id)
);


# Initial data
INSERT INTO customer (id, name, nickname, email, customer_status, customer_type)
VALUES (null, 'Yuichi Kageyama', 'Yuichi', 'kage.you@gmail.com', 'valid', 'internal');

INSERT INTO services(id, name, nickname, price)
VALUES (null, '開発テスト', 'test-0', 0);

INSERT INTO node(id, node_name, registration_code, customer)
VALUES (null, 'Arduino MKR1010', 'E7476F72-0824-4E65-8F16-4548DC03326E', 1);

INSERT INTO data(id, node, data_type, data_category, data_value, daq_datetime)
VALUES (null, 1, 'DAQ', 'test', 1.2, '2022-12-01 12;34;56');


# Users
GRANT ALL ON alice_services.* TO alice;