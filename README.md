# A very simple storage app
## What is this?
A simple web app that I use to keep track of everything we have in our storage room in the basement. It's a Flask-based Dockerized app with a SQLite database. In my case, it is hosted on Firebase, and thus the manual also shows you how to deploy it to Firebase. If you want to host it somewhere else, you'll have to make the appropriate changes.

## Can I use this for myself?
Sure, it's MIT licensed, so you can basically do what you want with it. 

However, I'm still working on a few things that you should be aware of before using this app. Most importantly, the database has not yet been persisted, which means that if you upload the app to a server with your personal content, then modify the database by adding or removing items in the database, your updates will disappear if the server crashes, or you deploy an update to the codebase to the server. Obviously, this is one of the most important things I'll be working on ASAP.

Also, there's no user authentication for the app, meaning that if you deploy it to Firebase, it will be totally public, and anyone who gets the link can modify the content of the database. So please don't store any sensitive information. 

## How do I run this?
As mentioned above it's built with Flask, using a SQLite database, then deployed to Firebase. This means that you must have a Google account and a Firebase project to host the app. Please refer to Google's documentation on how to create a Firebase project. Then you'll also need a CSV file that lists all the items you currently have in your storage. 

Here's a more detailed outline on how to get started:
1. Create a Firebase project with your Google account (please refer to Google's documentation on how to do so). Since only my family has to have access to the app, 
2. Git clone this repository
3. Provide your own categories and storage list:
  - Create a CSV file that lists all the items you currently have in your storage, and save it in the project's main directory. The CSV file must have the following columns, in this particular order: Category, article, quantity, expiry date. To keep things simple, the expiry date is simply formatted as YYMM. If the item does not have an expiry date, I suggest you set it to 9999.
  -  Create a .py file called 'categories_and_csv.py'(the name of the file is already in the gitignore since it contains the user's personal categories). In this file, you create two variables:
    - One called categories, which must be a list of lists. Each list within the list must have the following format: [category_id, category_name]. The category_id must be an integer, and the category_name should be a string.
    - One called storage_csv. This must be a string that refers to the CSV file created in the previous step, e.g. my_storage.csv.
4. Run the init_db.py file to create the database. Note that if you have previously run this script, re-running it will delete the database file before creating a new one. 

