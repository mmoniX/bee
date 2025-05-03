-- Create the database
CREATE DATABASE bee_pgdb;

-- Switch to the database (not needed in PostgreSQL scripts, but useful in psql CLI)
-- \c bee_db;

-- Create the sensor_type_tbl table
CREATE TABLE sensor_type_tbl (
    id SERIAL PRIMARY KEY,
    sensor_type_name VARCHAR(50) NOT NULL UNIQUE,
    serial_no VARCHAR(50) UNIQUE,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the beehive_tbl table
CREATE TABLE beehive_tbl (
    id SERIAL PRIMARY KEY,
    beehive_name VARCHAR(50) NOT NULL UNIQUE,
    sensor_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the measurement_unit_tbl table
CREATE TABLE measurement_unit_tbl (
    id SERIAL PRIMARY KEY,
    measurement_unit DECIMAL(8, 2) NOT NULL,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the location_tbl table
CREATE TABLE location_tbl (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(50) NOT NULL,
    location_cord VARCHAR(50) NOT NULL UNIQUE,
    descriptions VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the sensors_tbl table
CREATE TABLE sensors_tbl (
    id SERIAL PRIMARY KEY,
    beehive_id INT NOT NULL,
    sensor_type_id INT NOT NULL,
    sensor_name VARCHAR(50) NOT NULL,
    location_id INT NOT NULL,
    installation_date DATE NOT NULL,
    measurement_unit_id INT NOT NULL,
    last_seen TIMESTAMP,
    is_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_type_id) REFERENCES sensor_type_tbl (id) ON DELETE NO ACTION,
    FOREIGN KEY (measurement_unit_id) REFERENCES measurement_unit_tbl (id) ON DELETE NO ACTION,
    FOREIGN KEY (beehive_id) REFERENCES beehive_tbl (id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location_tbl (id) ON DELETE NO ACTION
);

-- Create the reading_tbl table
CREATE TABLE reading_tbl (
    id SERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    reading_value DECIMAL(10, 2) NOT NULL,
    reading_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors_tbl (id) ON DELETE CASCADE
);
