# Use cases of deadline-tracker

The goal of deadline-tracker is to make keeping track of deadlines simple for users, while offering useful functionality for both the regular and power users. On the most basic level, users will be able to add deadlines, tasks that must be completed before a certain date and time, and mark them as done.  

The deadlines can be grouped into categories, and divided into tasks that must all be completed before the deadline. The deadlines are also given a priority, ranging from "would be nice to get done" to "must absolutely get done". 

Existing tasks can sorted and selected by their categories, priorities and required time of completion.


## Use cases and the respective SQL-queries

### Adding a deadline

The most fundamental use of Deadline-tracker is adding a new deadline. 

If the user has the id 16, and is adding a deadline called "Course work", that must be completed by 2032-01-07 12:00, has an urgent priority, and belongs to a new category called "Uni", the following SQL-queries are used by the application.

~~~~sql
INSERT INTO Deadline (date_time, name, priority, done, account_id)
	VALUES (2032-01-07 12:00:00, "Course work", 3, False, 16);
~~~~

The application checks if the category already exists

~~~~sql
SELECT * FROM Category 
	WHERE account_id = 16 AND name = "Uni";
~~~~

In this case the query returns no results, so the new category is created.
~~~~sql
INSERT INTO Category (name, account_id) 
	VALUES ("Uni", 16);
~~~~

Finally the relation between the deadline and category is created, using the automatically created id's.

~~~~sql
INSERT INTO Deadline_category (deadline_id, category_id)
	VALUES (1, 1);
~~~~

### Viewing the deadlines

The default view, when all the user's deadlines are displayed. Here we assume the user's id to be 16 again.

~~~~sql 
SELECT * FROM Deadlines WHERE account_id = 16;
~~~~

If the user wants to only view urgent deadlines, in an ascending order by the date.

~~~~sql
SELECT * FROM Deadline
	WHERE account_id = 16 AND priority = 3
	ORDER BY date_time ASC;
~~~~

### Setting a deadline as done
~~~~sql
UPDATE Deadline
	SET done = true
	WHERE id = 1 AND account_id = 16;
~~~~
