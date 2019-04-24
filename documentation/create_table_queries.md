# All SQL CREATE TABLE-queries used in the application.

~~~~sql
CREATE TABLE Account (
	id INTEGER PRIMARY KEY,
	date_created DATETIME,
	date_modified DATETIME,
	username STRING,
	password STRING
);
~~~~

~~~~sql
CREATE TABLE Deadline (
	id INTEGER PRIMARY KEY,
	name STRING,
	date_time DATETIME,
	done BOOLEAN,
	priority INTEGER,
	account_id INTEGER
	FOREIGN KEY (account_id) REFERENCES Account(id)
);
~~~~

~~~~sql
CREATE TABLE Category (
	id INTEGER PRIMARY KEY,
	name STRING,
	priority INTEGER
);
~~~~

~~~~sql 
CREATE TABLE Category_deadline (
	deadline_id INTEGER,
	category_id INTEGER,
	FOREIGN KEY (deadline_id) REFERENCES Deadline(id),
	FOREIGN KEY (category_id) REFERENCES Category(id)
);
~~~~
