# A very simple storage app
## What is this?
A simple web app that I use to keep track of everything we have in our storage room in the basement. It's a Flask-based Dockerized app with a SQLite database. In my case, it is hosted on Firebase.

## Can I use this for myself?
Sure, it's MIT licensed, so you can basically do what you want with it, just don't sue me. You should note, however, that I'm far from done with it. In fact, this is the first real coding project I have made that is actually in real use. So quite a few things still need to be done - the most important being to persist the database (scroll down to the improvements section for more on this).

## How do I run this?
As mentioned above it's built with Flask, using a SQLite database. If you want to use it, you first have to create a CSV file with all your items, and then run 'python init_db.py' from the project's root directory. This should create the database and then store everything from your CSV file in it. If you have stored the items in the CSV file with columns that are not named Category, Article, Quantity and Expiry_date, you'll have to update the templates/frontpage.html file accordingly.

Very soon, I will change from Firebase to self-hosted, and then I will provide a more detailed instruction on how to set up this app.

BTW, I don't use a custom URL. The URL is assigned automatically by Google, when you deploy it to Firebase.


## OK, so how will this app be improved?
As with everything else, there's always room for improvement. But two very important things are pretty urgent: Persisting the database and separating the database in a second container.  Maybe you ask yourself how on earth I use an app with such a fundamental requirement not being fulfilled. My answer to that is that yes, in a way you're right - but at the end of the day, I prefer to have it up and running and then update it when I have time. 

So for now, just don't use it for anything vital - if your server breaks down, chances are you lose any updates made to the database since you deployed the app.

When I'm done with that, I think I'd like to add some kind of shopping cart so I can make a list of things I wanna get before I actually physically leave my apartment (this obviously also includes an option to empty the cart if I decide to leave things where they are).  Of course I also plan to implement a functionality that allows updating the content of the database without redeployment, to make it have more pages so that things can be viewed according to category, and a way to receive messages when something is close to its expiry date.

And then I'm also planning to set up CI/CD for this app (to learn how to use a sledgehammer, why not start by cracking a nut?).
