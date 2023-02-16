CREATE TABLE posts (
	id SERIAL PRIMARY KEY,
	title VARCHAR(50) NOT NULL,
	content VARCHAR(150) NOT NULL,
	published BOOLEAN DEFAULT FALSE,
	created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO posts (title, content) values ('Hello World', 'Supported Versions');