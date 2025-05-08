/* 2025-05-08 15:07:18 [11 ms] */ 
CREATE TABLE sensor_type_tbl (
    id UUID PRIMARY KEY,
    sensor_type_name VARCHAR(50) NOT NULL UNIQUE,
    serial_no VARCHAR(50) UNIQUE,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
/* 2025-05-08 15:07:38 [3 ms] */ 
CREATE TABLE measurement_unit_tbl (
    id UUID PRIMARY KEY,
    measurement_unit DECIMAL(8, 2) NOT NULL,
    descriptions VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
/* 2025-05-08 15:07:41 [4 ms] */ 
CREATE TABLE location_tbl (
    id UUID PRIMARY KEY,
    location_name VARCHAR(50) NOT NULL,
    location_cord VARCHAR(50) NOT NULL UNIQUE,
    descriptions VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
/* 2025-05-08 15:12:02 [8 ms] */ 
CREATE TABLE sensors_tbl (
    id UUID PRIMARY KEY,
    sensor_type_id UUID NOT NULL,
    sensor_name VARCHAR(50) NOT NULL,
    location_id UUID NOT NULL,
    installation_date DATE NOT NULL,
    measurement_unit_id UUID NOT NULL,
    last_seen TIMESTAMP,
    is_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sensor_type_id) REFERENCES sensor_type_tbl (id) ON DELETE NO ACTION,
    FOREIGN KEY (measurement_unit_id) REFERENCES measurement_unit_tbl (id) ON DELETE NO ACTION,
    FOREIGN KEY (location_id) REFERENCES location_tbl (id) ON DELETE NO ACTION
);
/* 2025-05-08 15:15:48 [5 ms] */ 
CREATE TABLE beehive_tbl (
    id UUID PRIMARY KEY,
    beehive_name VARCHAR(50) NOT NULL UNIQUE,
    sensor_id UUID NOT NULL, 
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    Foreign Key (sensor_id) REFERENCES sensors_tbl(id) ON DELETE cascade
);
