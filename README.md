# JobTrack
#### Video Demo:  <(https://youtu.be/QYgZ6pX00Yw)>
#### Description:

This is JobTrack! A web application that allows users to keep track of their job applications in one place. built as my final project for CS50.

I decided to build JobTrack because I wanted to build something that actually had a purpose beyond just being a project that I would finish and never look at again. Around the time internships and entry-level jobs start dropping students and newgrads can find themselves applying to tens and hundreds of applications a day. That's why JobTrack was built. for keeping track of different companies, positions, application links, locations, and hiring stages at the same time. I wanted JobTrack to provide a simple place where all of this information could be kept together.

## How JobTrack Works

Users can create an account using an email address, username, and password. After logging in, the user is taken to the main page where they can add and manage their job applications.

When adding an application, the user can provide the job title, company, job posting URL, company URL, location, status, and notes. The application can then be updated as the hiring process progresses.

JobTrack currently supports the following application statuses:

* Saved
* Applied
* Phone Screen
* Interview
* Offer
* Rejected
* Withdrawn
* Accepted

I chose these statuses because they cover the major stages that an application can go through without trying to make the hiring process unnecessarily complicated. The interview stage can mean different things depending on the company. Some companies may have two interviews, others may have three, while some companies may make a decision after a single interview. That's why instead of creating a separate status for every possible stage, Its much simpler to keep the application status more broad and have the user put those specific details in the notes associated with an application if needed.

Users can also update their notes or delete applications if needed. 

The account page provides an overview of the user's account, including their username, email, number of applications, job titles, and companies they have applied to. It also gives users control over their account through features such as changing their password, logging out, and deleting their account.

## Database

JobTrack uses SQLite as its database. For a project of this scale. I didn't see a reason to introduce a heavier database system when SQLite provides everything the application needs.

The database is organized around three main tables: `users`, `companies`, and `applications`.

The `users` table stores each user's email, username, password hash, and account creation time. Passwords are not stored as plain text, they are hashed before being stored in the database.

The `companies` table stores company names and their URLs. Companies have their own table instead of storing the company name directly inside every application. This prevents unnecessary duplication.

The `applications` table stores the actual job applications. Each application has a `user_id` and a `company_id`, which connect it to the user who created it and the company it belongs to. It also stores information such as the job title, job URL, location, status, application date, and notes.

This database structure helped me understand relational databases much better. Instead of thinking about the database as one large table, I had to think about how different pieces of information relate to each other and how SQL can be used to retrieve information across those relationships.

## Files

### `app.py`

`app.py` contains the main Flask application. It is responsible for creating the Flask app, sessions and CSRF protection, connecting to the SQLite database, and defining the application's routes.

The routes in this file handle registration, login, logout, adding applications, updating application statuses, updating notes, deleting applications, viewing the account page, changing passwords, and deleting accounts.

`app.py` also handles the database queries used to create, retrieve, update, and delete information. It checks the logged-in user's ID when modifying or deleting applications so that a user cannot simply provide another application's ID and modify someone else's data.

### `helpers.py`

`helpers.py` contains functions that are used across the entire application.

One function validates email addresses during registration. The other is the `login_required` decorator, which checks whether a user has a `user_id` stored in their session before allowing them to access routes that require authentication.

I kept these functions separate from `app.py` to keep everything organized.

### `templates/`

The `templates` directory contains the HTML pages used by Flask and Jinja.

`index.html` acts as the base template for the application. Other templates extend it so that common elements such as the navigation bar do not have to be written repeatedly.

`login.html` and `register.html` contain the login and registration interfaces.

`main.html` is the main part of the application where users can view, add, update, and delete their job applications.

`account.html` contains the user's account information and account management features.

`flash.html` is used to display Flask flash messages to the user.

The templates also use Bootstrap for styling and responsive layout, as well as JavaScript for some client-side interactions such as confirmation modals and password validation.

## Security and Authentication

Authentication was an important part of JobTrack. I learned a lot about authentication and security while working on CS50, especially during the Finance problem which was a part of pset9, and applied those concepts to this project.

Passwords are hashed using Werkzeug rather than being stored directly. Sessions are used to remember which user is currently logged in, and routes that require authentication are protected with the `login_required` decorator.

I also learned about CSRF protection while building JobTrack. POST requests that perform actions such as modifying or deleting data must include CSRF tokens.

JobTrach makes sure that users can only modify their own applications. Database queries for updating and deleting applications include both the application ID and the current user's ID. Knowing another application's ID is not enough to modify it.

## Why Flask and Bootstrap?

I chose Flask because I like frameworks that are relatively simple and bare-bones. Compared to larger Python web frameworks such as Django, Flask gives me more control over how the application is put together without introducing as much structure that I do not necessarily need for a project like this.

This is also part of why C was my favorite language during CS50. I generally enjoy working with tools that are closer to the underlying concepts instead of ones that are too bloated and try to handle everything for me.

Bootstrap was used mainly because responsive frontend development has always been one of my weaker areas. Even though i have more experience with Tailwind CSS, I wanted to use Bootstrap for this project and learn something different and to try out bootstrap's  responsive layout system.

The hardest part of the project for me was probably JavaScript. It felt very different from the other programming languages I had worked with during the course, and I found it much harder to reason about at first. Even though JavaScript is not my favorite language, I learned that some actions are much easier and lighter to implement on the client side rather than sending every small interaction back through Flask.

## What I Learned

One of the biggest things I gained from this project was more confidence with Python. Working on a complete application instead of individual problem sets.

I also learned a lot more about relational databases. Designing the tables and then actually using relationships between them made concepts such as primary keys, foreign keys, joins, and queries much easier to understand.

Authentication and security were another major area of learning. I had to think about password hashing, sessions, authorization, CSRF protection, and making sure users could only access their own data.

Finally, this project helped me understand what kind of development I enjoy. I found myself much more interested in the server-side and infrastructure aspects of the application than the frontend and UI work. Building the backend logic and database was much more enjoyable for me than dealing with JavaScript and responsive design. That has given me a better idea of the direction I may want to explore in the future.

## Future Improvements

If I continued developing JobTrack, one feature I would particularly like to explore is integrating it with LinkedIn and multiple other job platforms. Ideally, users could get notified when a new opportunity gets released on any job site. and maybe offer a premium service where a user can auto apply to the jobs with certain titles the user specifies beforehand
 
There are also smaller improvements I could make to the existing application, such as adding more ways to filter and organize applications and improving some of the frontend interactions and maybe adding dark mode.

For now, however, I wanted the project to remain focused on its main purpose: giving users a simple way to organize their job applications.

## Conclusion

JobTrack started as a rough idea for a practical CS50 final project and gradually became a more complete application as I built it. It gave me experience with the process of actually building something rather than simply completing individual exercises. I had to make design decisions, debug problems, learn technologies that were unfamiliar to me, and figure out how the different parts of an application communicate with each other.

The project is something I could realistically see myself using, which was the main reason I chose to build it in the first place, maybe i can improve on it in the near future and host it online for everyone to use. who knows? but untill then this will have to do for now.

This was JobTrack!