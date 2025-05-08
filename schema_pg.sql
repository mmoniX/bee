-- Create the database
-- CREATE DATABASE bee_pgdb;

-- Switch to the database (not needed in PostgreSQL scripts, but useful in psql CLI)
-- \c bee_db;

-- Create the sensor_type_tbl table
CREATE TABLE sensor_type_tbl (
    id UUID PRIMARY KEY,
    sensor_type_name VARCHAR(50) NOT NULL UNIQUE,
    serial_no VARCHAR(50) UNIQUE,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Create the measurement_unit_tbl table
CREATE TABLE measurement_unit_tbl (
    id UUID PRIMARY KEY,
    measurement_unit DECIMAL(8, 2) NOT NULL,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the location_tbl table
CREATE TABLE location_tbl (
    id UUID PRIMARY KEY,
    location_name VARCHAR(50) NOT NULL,
    location_cord VARCHAR(50) NOT NULL UNIQUE,
    descriptions VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the sensors_tbl table
CREATE TABLE sensors_tbl (
    id UUID PRIMARY KEY,
    -- beehive_id INT NOT NULL,
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
    -- FOREIGN KEY (beehive_id) REFERENCES beehive_tbl (id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location_tbl (id) ON DELETE NO ACTION
);

-- Create the reading_tbl table
-- CREATE TABLE reading_tbl (
--     id UUID PRIMARY KEY,
--     sensor_id INT NOT NULL,
--     reading_value DECIMAL(10, 2) NOT NULL,
--     reading_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (sensor_id) REFERENCES sensors_tbl (id) ON DELETE CASCADE
-- );


-- Create the beehive_tbl table
CREATE TABLE beehive_tbl (
    timestamp 
    id UUID PRIMARY KEY UUID,
    beehive_name VARCHAR(50) NOT NULL UNIQUE,
    sensor_id INT NOT NULL,  --device_name
    rainGauge VARCHAR(20),
    lightIntensity VARCHAR(20),
    relativeHumidity DECIMAL(8,2),
    temperature  DECIMAL(8,2),
    pressure INT,
    windDirection INT,
    tempC1 DECIMAL(2,1),
    tempC2 DECIMAL(2,1),
    tempC3 DECIMAL(2,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    -- reading Data fom a beehive, needs a sensor iformation
    Foreign Key (sensor_id) REFERENCES sensors_tbl(id) ON DELETE cascade
);

