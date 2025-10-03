CREATE DATABASE IF NOT EXISTS wells_db;
USE wells_db;

-- Drop existing tables
DROP TABLE IF EXISTS stimulated_data;
DROP TABLE IF EXISTS wells;

-- wells
CREATE TABLE wells (
    api_no VARCHAR(20) PRIMARY KEY,
    file_name VARCHAR(100),
    well_file_no INT,
    operator VARCHAR(255),
    well_name VARCHAR(255),
    job_id VARCHAR(50),
    job_type VARCHAR(255),
    county VARCHAR(255),
    latitude VARCHAR(50),
    longitude VARCHAR(50),
    datum VARCHAR(50),
    well_status VARCHAR(100),
    well_type VARCHAR(100),
    closest_city VARCHAR(100)
);

-- stimulated_data
CREATE TABLE stimulated_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_no VARCHAR(20),
    date_simulated DATE,
    formation VARCHAR(255),
    top_ft INT,
    bottom_ft INT,
    stimulation_stages INT,
    volume BIGINT,
    volume_units VARCHAR(50),
    type_treatment VARCHAR(100),
    lbs_proppant BIGINT,
    maximum_treatment_pressure_psi INT,
    maximum_treatment_rate_bbls_per_min DECIMAL(10,2),
    details TEXT
);
