-- Drop tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS tips;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS checkins;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS business;

-- Create tables
CREATE TABLE business (
    business_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    address TEXT,
    city VARCHAR(255),
    state VARCHAR(255),
    postal_code VARCHAR(20),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    stars DOUBLE PRECISION,
    review_count INTEGER,
    is_open INTEGER,
    attributes JSONB,
    categories TEXT,
    hours JSONB
);

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    review_count INTEGER,
    yelping_since DATE,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    elite TEXT[],
    friends TEXT[],
    fans INTEGER,
    average_stars DOUBLE PRECISION,
    compliment_hot INTEGER,
    compliment_more INTEGER,
    compliment_profile INTEGER,
    compliment_cute INTEGER,
    compliment_list INTEGER,
    compliment_note INTEGER,
    compliment_plain INTEGER,
    compliment_cool INTEGER,
    compliment_funny INTEGER,
    compliment_writer INTEGER,
    compliment_photos INTEGER
);

CREATE TABLE checkins (
    business_id VARCHAR(255) REFERENCES business(business_id),
    date TEXT,
    PRIMARY KEY (business_id, date)
);

CREATE TABLE reviews (
    review_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    business_id VARCHAR(255) REFERENCES business(business_id),
    stars DOUBLE PRECISION,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    text TEXT,
    date DATE
);

CREATE TABLE tips (
    user_id VARCHAR(255) REFERENCES users(user_id),
    business_id VARCHAR(255) REFERENCES business(business_id),
    text TEXT,
    date DATE,
    compliment_count INTEGER,
    PRIMARY KEY (user_id, business_id, date)
);