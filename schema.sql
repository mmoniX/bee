
CREATE DATABASE bee_db;

use bee_db;


CREATE TABLE sensor_type_tbl(
    id int not null PRIMARY KEY,
    sensor_type_name varchar(50) not null UNIQUE,
    serial_no varchar(50) UNIQUE,
    descriptions varchar(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE measurement_unit_tbl(
    id int not null PRIMARY KEY,
    measurement_unit decimal(8,2) NOT NULL,
    descriptions VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE location_tbl(
    id int not null PRIMARY KEY,
    location_name varchar(50) NOT NULL,
    location_cord varchar(50) NOT NULL UNIQUE,
    descriptions varchar(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE sensors_tbl(
    id int not null PRIMARY KEY,
    sensor_type_id int not null,
    sensor_name VARCHAR(50) UNIQUE not null,
    location_id varchar(50) NOT NULL,
    installation_date DATE not null,
    measurement_unit_id int not null,
    last_seen DATETIME,
    is_active boolean,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY(sensor_type_id) REFERENCES sensors_type_tbl(id) on delete cascade,
    FOREIGN KEY(measurement_unit_id) REFERENCES measurement_unit_tbl(id) on delete No action,
    FOREIGN KEY(location_id) REFERENCES location_tbl(location_id) on delete NO action
);

CREATE TABLE sensors_tbl(
    id int not null PRIMARY KEY,
    beehive_id int not null,
    sensor_type_id int not null,
    sensor_name VARCHAR(50) not null,
    location_id varchar(50) NOT NULL,
    installation_date DATE not null,
    measurement_unit_id int not null,
    last_seen DATETIME,
    is_active boolean,
    

    FOREIGN KEY(sensor_type_id) REFERENCES sensor_type_tbl(sensor_type_id) on delete No action,
    FOREIGN KEY(measurement_unit_id) REFERENCES measurement_unit_tbl(measurement_unit_id) on delete No action,
    FOREIGN KEY(beehive_id) REFERENCES beehive_tbl(beehive_id) on delete No action,
    FOREIGN KEY(location_id) REFERENCES location_tbl(location_id) on delete No action
);
