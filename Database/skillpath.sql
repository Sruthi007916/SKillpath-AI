CREATE DATABASE IF NOT EXISTS skillpath_ai;
USE skillpath_ai;

CREATE TABLE IF NOT EXISTS users (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profiles (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT UNIQUE NOT NULL,
    education  VARCHAR(100),
    department VARCHAR(100),
    skills     TEXT,
    interests  TEXT,
    language   VARCHAR(50) DEFAULT 'English',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS assessments (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNIQUE NOT NULL,
    technical     INT DEFAULT 0,
    communication INT DEFAULT 0,
    aptitude      INT DEFAULT 0,
    logical       INT DEFAULT 0,
    domain        INT DEFAULT 0,
    overall       INT DEFAULT 0,
    level         VARCHAR(20) DEFAULT 'Beginner',
    taken_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);