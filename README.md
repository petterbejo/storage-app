# A very simple storage app
## What is this?
A simple web app that I use to keep track of everything we have in our storage room in the basement. It's a Flask-based containerized app with a SQLite database. 

## Can I use this for myself?
Of course! But please be aware of two things: 

- There's no user authentication for the app, meaning that if you host it somewhere, it will be totally public, and anyone who gets the link can modify the content of the database. So please don't use the app to store any sensitive information. 
- Even if it uses a Docker volume to store the DB content on the host, everything (the Flask app and the DB) is still run within a single container, meaning that you risk losing your changes if you redeploy your instance. Use the export functionality to backup your content before making any changes to the installation!

## How do I run this?
As mentioned above it's built with Flask, using a SQLite database. You need a CSV file that lists all the items you currently have in your storage to fill the database with your personal content. 

There are basically two ways of getting started:
1 Get the images from my repo on Docker Hub: https://hub.docker.com/r/petterbejo/storage-app and deploy it wherever you wish. 
2 Git clone this repository (if you want to build the images yourself) and build the image by running the Docker build commands from within the webapp directory.

Once you've got it up and running, you have to go to your_url/run_db_setup. This will create the database. If you go to the main page before, you will get an error!

Then you will have to fill in the categories. Once you have created them, you can go to the main page and make a bulk upload with a CSV file. The CSV file must have the following columns, in this particular order: Category, article, quantity, expiry date. To keep things simple, the expiry date is simply formatted as YYMM. If the item does not have an expiry date, I suggest you set it to 9999. The delimiter must be a semi-colon. If the category is not written exactly the same way you did when you filled in the categories, the item will not be inserted. So be aware of spaces and cases!

## How will the app be improved?
Here are some ideas that I'd like to implement at some point in the future:

- I'd like to add some kind of shopping cart so I can make a list of things I wanna get before I actually physically leave my apartment (this obviously also includes an option to empty the cart if I decide to leave things where they are)
- A proper CI/CD pipeline that builds the images, pushes them to Docker Hub and tests the applications inside a container 
- A way of receiving a message when an item is close to its expiry date
