CREATE DATABASE expense_tracker_chatbot;

-- Connect to the new database
\c expense_tracker_chatbot;

-- Create a tracker schema
CREATE SCHEMA IF NOT EXISTS tracker;

-- Create an "expense" table
CREATE TABLE IF NOT EXISTS tracker.expense (
    category VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL,
    date DATE NOT NULL
);