CREATE TABLE urls (
    id bigint PRIMARY KEY,
    name varchar(255) UNIQUE,
    created_at datatime
);