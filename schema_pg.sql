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
    -- measurement_unit DECIMAL(8, 2) NOT NULL,
    measurement_unit VARCHAR(50) NOT NULL UNIQUE,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the location_tbl table
CREATE TABLE location_tbl (
    id UUID PRIMARY KEY,
    location_name VARCHAR(50) NOT NULL UNIQUE,
    -- location_cord VARCHAR(50) NOT NULL UNIQUE,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the sensors_tbl table
CREATE TABLE sensors_tbl (
    id UUID PRIMARY KEY,
    -- beehive_id INT NOT NULL,
    sensor_type_id UUID NOT NULL,
    sensor_name VARCHAR(200) NOT NULL UNIQUE,
    location_id UUID NOT NULL,
    installation_date DATE NOT NULL,
    measurement_unit_id UUID NOT NULL,
    last_seen TIMESTAMP,
    is_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sensor_type_id) REFERENCES sensor_type_tbl (id) ON DELETE NO ACTION,
    FOREIGN KEY (measurement_unit_id) REFERENCES measurement_unit_tbl (id) ON DELETE NO ACTION,
    -- FOREIGN KEY (beehive_id) REFERENCES beehive_tbl (id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location_tbl (id) ON DELETE NO ACTION
);

-- Create the beehive_tbl table
CREATE TABLE beehive_tbl (
    id UUID PRIMARY KEY,
    beehive_name VARCHAR(50) NOT NULL,
    sensor_id UUID NOT NULL,  --device_name
    -- lightIntensity FLOAT,
    -- rainGauge FLOAT,
    -- relativeHumidity FLOAT,
    -- temperature FLOAT,
    -- pressure FLOAT,
    -- windDirection FLOAT,
    -- uvIndex FLOAT,
    -- windSpeed FLOAT,
    -- tempC1 FLOAT,
    -- tempC2 FLOAT,
    -- tempC3 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- reading Data fom a beehive, needs a sensor iformation
	CONSTRAINT unique_beehive_sensor UNIQUE (beehive_name, sensor_id),
    FOREIGN KEY (sensor_id) REFERENCES sensors_tbl (id) ON DELETE CASCADE
);

-- Create reading_tbl
CREATE TABLE reading_tbl (
    id UUID PRIMARY KEY,
    beehive_id UUID NOT NULL,
    ts TIMESTAMP NOT NULL,
    feature_name VARCHAR(50) NOT NULL,
    reading_value FLOAT NOT NULL,
    measurement_unit_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (beehive_id) REFERENCES beehive_tbl (id) ON DELETE CASCADE,
    FOREIGN KEY (measurement_unit_id) REFERENCES measurement_unit_tbl (id)
);