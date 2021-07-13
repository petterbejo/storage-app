# A very simple storage app
## What is this?
A simple web app that I use to keep track of everything we have in our storage room in the basement. It's a Flask-based app with a SQLite database. Previously, I hosted it on Firebase, with the whole app in a single container. Obviously, this is not the best solution, so right now I am working on turning the project into a multi-container app.

## Can I use this for myself?
Sure, it's MIT licensed, so you can basically do what you want with it. 

However, I'm still working on a few things that you should be aware of before using this app. Most importantly, the database has not yet been persisted, which means that if you upload the app to a server with your personal content, then modify the database by adding or removing items in the database, your updates will disappear if the server crashes, or you deploy an update of the codebase to the server. 

Also, there's no user authentication for the app, meaning that if you host it somewhere, it will be totally public, and anyone who gets the link can modify the content of the database. So please don't use the app to store any sensitive information. 

## How do I run this?
As mentioned above it's built with Flask, using a SQLite database. You need a CSV file that lists all the items you currently have in your storage to fill the database with your personal content. 

Since the project is work in progress, I can't provide a detailed step-by-step guide on how to get started. However, the following steps (in no particular order) will almost certainly be part of the process:

- Get the images from my repo on Docker Hub. Git clone this repository (if you want to build the images yourself).
- Provide your own categories and storage list:
  - Create a CSV file that lists all the items you currently have in your storage, and save it in the project's main directory. The CSV file must have the following columns, in this particular order: Category, article, quantity, expiry date. To keep things simple, the expiry date is simply formatted as YYMM. If the item does not have an expiry date, I suggest you set it to 9999.
  -  Create a .py file called 'categories_and_csv.py'(the name of the file is already in the gitignore since it contains the user's personal categories). In this file, you create two variables:
    - One called categories, which must be a list of lists. Each list within the list must have the following format: [category_id, category_name]. The category_id must be an integer, and the category_name should be a string.
    - One called storage_csv. This must be a string that refers to the CSV file created in the previous step, e.g. my_storage.csv.
- Run the init_db.py file to create the database. Note that if you have previously run this script, re-running it will delete the database file before creating a new one. 

## How will the app be improved?
Here are some ideas that I'd like to implement at some point in the future:

- I'd like to add some kind of shopping cart so I can make a list of things I wanna get before I actually physically leave my apartment (this obviously also includes an option to empty the cart if I decide to leave things where they are)
- View items according to category
- A proper CI/CD pipeline that builds the images, pushes them to Docker Hub and tests the applications inside a container 
- A way of receiving a message when an item is close to its expiry date
- A proper handling of dependencies, e.g. with Pipenv
