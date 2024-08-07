# Define a configuration class for the Flask application
class Config:
    # Secret key used for session management and cryptographic signatures
    SECRET_KEY = 'your_secret_key'

    # Database URI for SQLAlchemy to connect to PostgreSQL database
    # Format: 'postgresql+driver://username:password@host/database_name'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:801633@localhost/url_shortener'

    # Disable modification tracking for SQLAlchemy to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
