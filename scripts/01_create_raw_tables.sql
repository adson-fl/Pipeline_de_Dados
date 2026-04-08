CREATE TABLE raw_usuarios (
    id INTEGER PRIMARY KEY,
    name VARCHAR (255),
    username VARCHAR (255),
    email VARCHAR (255),
    address_street VARCHAR (255),
    address_city VARCHAR (255),
    address_zipcode, VARCHAR (255),
    phone VARCHAR (50),
    wabsite VARCHAR (255),
    company_name VARCHAR (255),
    dl_load_timestamp TIMESTAMP 
);

CREATE TABLE raw_posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT,
    dl_load_timestamp TIMESTAMP
);