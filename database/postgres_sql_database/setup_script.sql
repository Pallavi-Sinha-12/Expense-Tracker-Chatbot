-- Create a new role (user) with a password
CREATE ROLE expense_user WITH LOGIN PASSWORD '<your_password>';

-- Create a new database
CREATE DATABASE expense_tracker_chatbot;

-- Connect to the new database
\c expense_tracker_chatbot;

-- Create a tracker schema
CREATE SCHEMA IF NOT EXISTS tracker;

-- Create an "expense" table
CREATE TABLE IF NOT EXISTS tracker.expense (
    category VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL,
    expense_date DATE NOT NULL
);

-- Grant necessary privileges to the user
GRANT ALL PRIVILEGES ON DATABASE expense_tracker_chatbot TO expense_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA tracker TO expense_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA tracker TO expense_user;