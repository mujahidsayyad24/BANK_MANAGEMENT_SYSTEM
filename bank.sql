create database BANK_MANAGEMENT;
USE BANK_MANAGEMENT;
CREATE TABLE users (
    account_no BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    balance BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE transactions (
    trans_id INT PRIMARY KEY AUTO_INCREMENT,
    account_no BIGINT,
    trans_type VARCHAR(10) NOT NULL,
    amount BIGINT NOT NULL,
    trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_no) REFERENCES users(account_no)
);
