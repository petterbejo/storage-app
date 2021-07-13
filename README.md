# A simple storage app
## What is this?
A simple web app that I use to keep track of everything we have in our storage room in the basement. It's a Flask-based Dockerized app with a SQLite database.

I'm currently working on turning this into a multi-container app. The other branches of this project are all steps on the way to achieve this.


## Can I use this for myself?
Sure, it's MIT licensed, so you can basically do what you want with it. 

However, I'm still working on a few things that you should be aware of before using this app. Most importantly, the database has not yet been persisted, which means that if you upload the app to a server with your personal content, then modify the database by adding or removing items in the database, your updates will disappear if the server crashes, or you deploy an update to the codebase to the server. Obviously, this is one of the most important things I'll be working on ASAP.

Also, there's no user authentication for the app, meaning that if you host it somewhere, it will be totally public, and anyone who gets the link can modify the content of the database. So please don't store any sensitive information. 

Soon, I hope to provide information on how to run this app.
