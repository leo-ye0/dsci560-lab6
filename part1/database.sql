CREATE DATABASE IF NOT EXISTS wells_db;
USE wells_db;

-- Drop existing tables (handle foreign key constraints)
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS stimulated_data;
DROP TABLE IF EXISTS wells;
DROP TABLE IF EXISTS stimulations;
SET FOREIGN_KEY_CHECKS = 1;

-- wells
CREATE TABLE wells (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    api_no VARCHAR(50),
    well_status VARCHAR(100),
    well_type VARCHAR(100),
    closest_city VARCHAR(255),
    county VARCHAR(255),
    lat_long VARCHAR(100),
    oil_prod DECIMAL(10,2),
    gas_prod DECIMAL(10,2)
);

-- stimulated_data 
CREATE TABLE stimulated_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id VARCHAR(50),
    api_no VARCHAR(50),
    date_stimulated DATE,
    stimulated_formation TEXT,
    top_ft INT,
    bottom_ft INT,
    stimulation_stages INT,
    volume BIGINT,
    volume_units VARCHAR(50),
    type_treatment TEXT,
    lbs_proppant BIGINT,
    maximum_treatment_pressure_psi INT,
    maximum_treatment_rate_bbls_per_min DECIMAL(10,2)
);
