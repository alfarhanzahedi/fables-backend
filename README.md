# Fables

Fables is a financial crowdsourcing platform designed to help small businesses keep their wheels running during these tough times.

## Install Instructions
0. `$ mkdir fables && cd fables`
1. Install `virtualenv`. Instructions can found here: https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b
2. `$ virtualenv venv`. If this command fails, try adding `virtualenv` to $path.
3. Activate the virtual environment `venv`. The command may differ depending on the OS. For Linux based systems, command is provided in the above link.
4. Clone the repository:
 `$ git clone https://github.com/alfarhanzahedi/fables-backend.git`

5. `$ cd fables-backend`

6. Install all the requirements. `$ pip install -r requirements/development.txt`

7. Create an `.env` file: `$ touch .env`.

8. Copy and paste the contents of `.env.example` to `.env`. You can modify the variables as per your own settings. However, for development purposes, modifications are not necessary. The preexisiting !

9. In another terminal tab, download and run MailHog from here: https://github.com/mailhog/MailHog/releases/v1.0.0.
MailHog is needed to capture emails in dev environment.

10. Run migrations: `$ python manage.py migrate`.

11. Run the development server: `$python manage.py runserver`.
