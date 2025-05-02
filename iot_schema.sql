CREATE TABLE fridge_data (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    moisture NUMERIC(5, 2),
    timestamp TIMESTAMPTZ NOT NULL
);
CREATE TABLE dishwasher_data (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    water_usage NUMERIC(6, 2),
    timestamp TIMESTAMPTZ NOT NULL
);
CREATE TABLE device_energy_data (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    electricity NUMERIC(6, 2),
    timestamp TIMESTAMPTZ NOT NULL
);
CREATE TABLE device_metadata (
    device_id INTEGER PRIMARY KEY,
    device_name TEXT,
    device_type TEXT,
    timezone TEXT DEFAULT 'UTC',
    unit TEXT
);
