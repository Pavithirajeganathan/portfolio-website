-- ============================================================
-- Pavithira J — Portfolio Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS portfolio_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE portfolio_db;

-- ------------------------------------------------------------
-- messages
-- Stores every submission from the site's contact form.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS messages (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(150)  NOT NULL,
    subject     VARCHAR(150)  NOT NULL,
    message     TEXT          NOT NULL,
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_messages_created_at (created_at),
    INDEX idx_messages_email (email)
) ENGINE=InnoDB;
