CampusConnect Chat Application

About the Project

CampusConnect is a chat application developed using Python Flask and MySQL. It allows users to create accounts, log in securely, and communicate with other users through private and group chats.

This project was built to learn full-stack web development concepts such as authentication, database connectivity, session management, and CRUD operations.

Features

User Registration and Login
Secure Password Hashing
Private User-to-User Chat
Group Chat
Search Users
Edit Messages
Delete Messages
Online / Offline Status
Last Seen Feature
Message Timestamps
Responsive User Interface

Technologies Used

Python,
Flask,
MySQL,
HTML,
CSS,
JavaScript,
Werkzeug Security

Database

The project uses MySQL with two tables:

users,
messages

The database structure is provided in `database.sql`.

Installation

1. Clone the repository.
2. Create the MySQL database using `database.sql`.
3. Install dependencies:

pip install -r requirements.txt

4. Open app.py and update the MySQL credentials:
password="YOUR_MYSQL_PASSWORD"
5. Run the application:

python app.py

Project Structure

chat-app/

├── app.py

├── database.sql

├── requirements.txt

├── static/

│ └── style.css

├── templates/

│ ├── login.html

│ ├── signup.html

│ ├── chat.html

│ └── edit.html

Future Improvements

* File Sharing
* Profile Pictures
* Real-Time Messaging
* Message Reactions
* Chat Notifications

Author

Developed as a learning project to practice Flask, MySQL, and full-stack web development concepts.
