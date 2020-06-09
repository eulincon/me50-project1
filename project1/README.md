# Project 1

Web Programming with Python and JavaScript

book.html - This page shows the selected book past the book id via the get method.

dashboard.html - This page represents the home page after the user is logged in. It contains the book's search field.

index.html - This is the home page for the user to enter their user and password data to access the book search and evaluation features.

layout.html - Layout used before the user was logged in.

layout_dash.html - Layout used for when the user is logged in. Also contains the navigation bar.

register.html - Page for the user to register by entering a username and password.

sucess_registration.html - Page informing that the user registration was completed successfully.



The first line of books.csv has been removed to import the data as the first line is only the column titles,
considering in the import.py file that the table already exists in the database.

In book.html and register.html a JQuery Validation Plugin was used to validate the form data preventing the user from entering a username with space.


db{
	host: ec2-52-202-146-43.compute-1.amazonaws.com
	database: dd5p7nll6b9cl
	user: qbkjeniegjvgtu
	password: 758c111dfd887d8c601d93a3d3fb854ec35412ef2605fde7a67b8741f4a428cc
	uri: postgres://qbkjeniegjvgtu:758c111dfd887d8c601d93a3d3fb854ec35412ef2605fde7a67b8741f4a428cc@ec2-52-202-146-43.compute-1.amazonaws.com:5432/dd5p7nll6b9cl
}