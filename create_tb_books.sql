CREATE TABLE tb_books(
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);

CREATE TABLE tb_users(
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL
);

CREATE TABLE tb_reviews(
  id SERIAL PRIMARY KEY,
  id_book INTEGER REFERENCES tb_books(id),
  id_user INTEGER REFERENCES tb_users(id),
  comment VARCHAR NOT NULL,
  rate INTEGER NOT NULL
);
