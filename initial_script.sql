CREATE ROLE chocolate_shop_username with password 'chocolate_pixies';
ALTER ROLE chocolate_shop_username WITH LOGIN;
CREATE DATABASE chocolate_shop WITH OWNER chocolate_shop_username;
GRANT ALL PRIVILEGES ON DATABASE chocolate_shop to chocolate_shop_username;
ALTER USER chocolate_shop_username CREATEDB;

