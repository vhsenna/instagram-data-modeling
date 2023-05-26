import psycopg2

# Database connection parameters
hostname = 'your_hostname'
username = 'your_username'
password = 'your_password'
database = 'instagram'


# Connect to the default PostgreSQL database
conn = psycopg2.connect(
    host=hostname,
    user=username,
    password=password,
)
conn.autocommit = True
cur = conn.cursor()


# Create the database
def create_database():
    try:
        query = f'CREATE DATABASE {database}'
        cur.execute(query)
        print(f"The database '{database}' was created successfully!")
    except (Exception, psycopg2.Error) as error:
        print('Error creating the database:', error)


# Create tables
def create_tables():
    try:
        # Connect to the instagram PostgreSQL database
        conn = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            database=database
        )
        conn.autocommit = True
        cur = conn.cursor()

        query = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL,
                phone_number VARCHAR(20) UNIQUE
            );

            CREATE TABLE IF NOT EXISTS posts (
                post_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                caption TEXT,
                image_url VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS comments (
                comment_id SERIAL PRIMARY KEY,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                comment_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(post_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS likes (
                like_id SERIAL PRIMARY KEY,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(post_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS followers (
                follower_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                follower_user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES posts(post_id),
                FOREIGN KEY (follower_user_id) REFERENCES users(user_id)
            );
        '''
        cur.execute(query)
        print('The tables were created successfully!')
    except (Exception, psycopg2.Error) as error:
        print('Error creating tables:', error)


# Call the functions to create the database and tables
create_database()
create_tables()

# Close the cursor and connection
cur.close()
conn.close()
