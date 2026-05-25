CREATE DATABASE traffic_db;
CREATE TABLE traffic_predictions (

    id SERIAL PRIMARY KEY,

    hour INTEGER,
    lat FLOAT,
    longi FLOAT,
    alert VARCHAR(100),
    speed FLOAT,

    prediction VARCHAR(50),
    suggestion VARCHAR(100)
);
select * from traffic_predictions;
