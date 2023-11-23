# A simple storage app
## What is this?

If you have a storage room with food and all kinds of goods that you'd like to keep track of, then this is the app for you. It's a Flask-based containerized app with a Postgres database. 

## Can I use this for myself?

Of course! But please be aware that there's no user authentication for the app, meaning that if you host it somewhere, it will be totally public, and anyone who gets the link can modify the content of the database. So please don't use the app to store any sensitive information. 

## How do I run this?

There are basically two ways of getting started:
1. Copy the `docker-compose.yaml` file to wherever you want to run the app, then run it with `docker-compose up -d`. This pulls the official Postgres image and the image from [my repo on Docker Hub](https://hub.docker.com/r/petterbejo/storage-app), and runs the app on port 5000 of the host machine. 
2. If you want to build the images yourself, clone this repository and build the image by running `docker-compose up -d` from the project's root directory.

Please note that no matter which of the two methods you choose, you must create a file called `db_password.txt` containing a password for the database. Docker Secrets will take care of the rest.

Once you've got it up and running, you have to go to `your_url/run_db_setup`. This will create the database and guide you through the setup process. If you go to the main page before, you will get an error!

Then you will have to fill in the categories. Once you have created them, you can go to the main page and make a bulk upload with a CSV file. The CSV file must have the following columns, in this particular order: Category, article, quantity, expiry date. To keep things simple, the expiry date is formatted as YYMM. If the item does not have an expiry date, I suggest you set it to 9999. The delimiter must be a semi-colon. If the category is not written exactly the same way you did when you filled in the categories, the item will not be inserted. So be aware of spaces and cases!

## How will the app be improved?

First of all, the app was one of the first projects I ever coded. This mainly means that the overall structure could benefit from a profound reworking. I'd also like to add some kind of shopping cart so I can make a list of things I wanna get before I actually physically leave my apartment (this obviously also includes an option to empty the cart if I decide to leave things where they are). Currently, I'm working on the option to insert a single new item.
