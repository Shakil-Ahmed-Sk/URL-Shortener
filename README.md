URL Shortener with Analytics

This is a Flask-based URL Shortener web application that allows users to shorten long URLs, track analytics such as click counts and referrers, and manage their shortened URLs through a dashboard. The application also supports user authentication and provides a secure environment for managing user data.

Table of Contents

Features

Technologies Used

How to Use

File Structure

Future Enhancements

Contact

Features

URL Shortening: Generate short, unique URLs for long links.

Analytics Dashboard: Track click counts, referrers, and timestamps for shortened URLs.

User Authentication: Secure user accounts with login and signup features.

Responsive Design: Optimized for desktop and mobile devices.

Database Integration: Stores user and URL data securely using SQLAlchemy.

Referrer Tracking: Logs referrers for detailed analytics.

Technologies Used

Python (Flask)

Flask-Login for user authentication

Flask-SQLAlchemy for database integration

Flask-Migrate for database migrations

Werkzeug for password hashing

HTML5 & CSS3 for frontend

How to Use

Clone the repository:

git clone https://github.com/your-username/url-shortener.git

Navigate to the project directory:

cd url-shortener

Install the required dependencies:

pip install -r requirements.txt

Set up the database:

flask db init
flask db migrate
flask db upgrade

Run the application:

flask run

Open the application in your browser at http://127.0.0.1:5000.

File Structure

URL Shortener
├── migrations               # Database migration files
├── static
│   └── styles.css          # Custom CSS for the application
├── templates
│   ├── dashboard.html      # Dashboard for URL analytics
│   ├── index.html          # Home page for URL shortening
│   ├── login.html          # Login page
│   ├── profile.html        # User profile page
│   ├── signup.html         # Signup page
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── models.py               # Database models
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation

Future Enhancements

Add support for custom short URLs.

Implement email verification for new user registrations.

Add charts for better analytics visualization.

Improve SEO for shortened URLs.

Deploy the application to a cloud platform.

Contact

Email: shakilahmedsk35@gmail.com

Phone: +91 7369-933912

Location: Plassey, Nadia, West Bengal, India

License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this application for personal or commercial purposes.
