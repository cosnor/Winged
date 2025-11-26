-- Crear las bases de datos necesarias para cada microservicio
CREATE DATABASE winged_users;
CREATE DATABASE winged_sightings;
CREATE DATABASE winged_maps;
CREATE DATABASE winged_routes;
CREATE DATABASE winged_achievements;

-- Grant permisos al usuario postgres
GRANT ALL PRIVILEGES ON DATABASE winged_users TO postgres;
GRANT ALL PRIVILEGES ON DATABASE winged_sightings TO postgres;
GRANT ALL PRIVILEGES ON DATABASE winged_maps TO postgres;
GRANT ALL PRIVILEGES ON DATABASE winged_routes TO postgres;
GRANT ALL PRIVILEGES ON DATABASE winged_achievements TO postgres;

-- Conectarse a winged_users y crear extensiones si es necesario
\c winged_users;
CREATE EXTENSION IF NOT EXISTS postgis;

\c winged_sightings;
CREATE EXTENSION IF NOT EXISTS postgis;

\c winged_maps;
CREATE EXTENSION IF NOT EXISTS postgis;