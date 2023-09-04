CREATE TYPE ruoli AS ENUM ('analyst', 'admin', 'specialist', 'developer');
create domain email_type as varchar check (value like '%@%.%');

CREATE OR REPLACE FUNCTION store_password()
RETURNS TRIGGER AS
$f$
    BEGIN
        new.password = sha512(new.password);
        RETURN new;
    END;
$f$
LANGUAGE plpgsql;

CREATE TABLE users(
  id serial not null primary key, 
  email email_type not null, 
  password bytea, 
  ruolo ruoli not null, 
  disponibilità boolean not null default true,
  score int not null default 0
);

CREATE OR REPLACE TRIGGER store_password
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION store_password();


INSERT INTO users (email, password, ruolo) VALUES ('matteo.rocco68@gmail.com', 'mattrocc68', 'analyst');
INSERT INTO users (email, ruolo) VALUES ('Rodfalanga@outlook.it', 'developer');
INSERT INTO users (email, ruolo) VALUES ('mario.armento01@gmail.com', 'specialist');
INSERT INTO users (email, ruolo) VALUES ('marziapirozzi2002@gmail.com', 'analyst');
INSERT INTO users (email, ruolo) VALUES ('ascolesealessia18@gmail.com', 'specialist');
