-- First create tables without dependencies
CREATE TABLE IF NOT EXISTS business (
    business_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    stars FLOAT,
    review_count INTEGER,
    is_open INTEGER,
    attributes JSONB,
    categories TEXT,
    hours JSONB
);

CREATE TABLE IF NOT EXISTS user_profile (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    review_count INTEGER,
    yelping_since TIMESTAMP,
    friends TEXT,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    fans INTEGER,
    elite TEXT,
    average_stars FLOAT,
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

-- Then create tables with foreign key dependencies
CREATE TABLE IF NOT EXISTS review (
    review_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    business_id VARCHAR(255),
    stars FLOAT,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    text TEXT,
    date TIMESTAMP,
    year INTEGER,
    month INTEGER,
    FOREIGN KEY (business_id) REFERENCES business(business_id),
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
);

CREATE TABLE IF NOT EXISTS tip (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    business_id VARCHAR(255),
    text TEXT,
    date TIMESTAMP,
    compliment_count INTEGER,
    year INTEGER,
    FOREIGN KEY (business_id) REFERENCES business(business_id),
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
);

CREATE TABLE IF NOT EXISTS checkin (
    id SERIAL PRIMARY KEY,
    business_id VARCHAR(255),
    date TEXT,
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

-- Finally create indexes
CREATE INDEX IF NOT EXISTS idx_business_location ON business(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_review_date ON review(date);
CREATE INDEX IF NOT EXISTS idx_tip_date ON tip(date);
CREATE INDEX IF NOT EXISTS idx_business_stars ON business(stars);