-- Database initialization script for FastAPI Vertical Slice
-- This script is run when PostgreSQL container starts

-- Create the main database if it doesn't exist
-- (This is typically handled by the POSTGRES_DB environment variable)

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create a simple users table for demonstration
-- (In a real app, this would be handled by Alembic migrations)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);

-- Insert sample data for development
INSERT INTO users (email, first_name, last_name, password_hash)
VALUES 
    ('admin@example.com', 'Admin', 'User', '$2b$12$placeholder_hash'),
    ('john@example.com', 'John', 'Doe', '$2b$12$placeholder_hash')
ON CONFLICT (email) DO NOTHING; 