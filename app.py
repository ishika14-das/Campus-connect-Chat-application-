from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "chatapp123"

# DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_MYSQL_PASSWORD",
    database="chat_app"
)

cursor = db.cursor()


# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        sql = """
        SELECT * FROM users
        WHERE username=%s
        """

        cursor.execute(
            sql,
            (username,)
        )

        user = cursor.fetchone()

        if user and check_password_hash(
            user[2],
            password
        ):

            session['username'] = username
            cursor.execute(
            """
            UPDATE users

            SET status='Online'

            WHERE username=%s
            """,

            (username,)
            )

            db.commit()
            return redirect(
                '/chat'
            )

        return render_template(
            'login.html',
            message="Invalid Username or Password"
        )

    return render_template(
        'login.html',
        message=""
    )


# SIGNUP
@app.route(
    '/signup',
    methods=['GET', 'POST']
)
def signup():

    if request.method == 'POST':

        username = request.form[
            'username'
        ]

        password = request.form[
            'password'
        ]

        hashed_password = generate_password_hash(
            password
        )

        check_sql = """
        SELECT * FROM users
        WHERE username=%s
        """

        cursor.execute(
            check_sql,
            (username,)
        )

        existing_user = cursor.fetchall()

        if existing_user:

            return render_template(
                'signup.html',
                message="Username already exists"
            )

        sql = """
        INSERT INTO users(
        username,
        password
        )

        VALUES(
        %s,
        %s
        )
        """

        values = (
            username,
            hashed_password
        )

        cursor.execute(
            sql,
            values
        )

        db.commit()

        return render_template(
            'login.html',
            message="Account Created Successfully"
        )

    return render_template(
        'signup.html',
        message=""
    )


# USER LIST
@app.route(
    '/chat',
    methods=['GET']
)
def chat():

    if 'username' not in session:

        return redirect('/')

    current_user = session[
        'username'
    ]

    sql = """
    SELECT username
    FROM users
    WHERE username != %s
    """

    cursor.execute(
        sql,
        (current_user,)
    )

    users = cursor.fetchall()

    return render_template(
        'chat.html',
        users=users,
        messages=[],
        current_user=current_user,
        selected_user=""
    )


# PRIVATE CHAT
@app.route(
'/chat/<selected_user>',
methods=['GET','POST']
)
def private_chat(selected_user):

    if 'username' not in session:
        return redirect('/')

    current_user = session['username']

    # Send message
    if request.method == 'POST':

        message = request.form['message']

        sql = """
        INSERT INTO messages
        (
        sender,
        receiver,
        message
        )

        VALUES
        (
        %s,
        %s,
        %s
        )
        """

        values = (
            current_user,
            selected_user,
            message
        )

        cursor.execute(
            sql,
            values
        )

        db.commit()

    # Load only private messages
    sql = """
    SELECT *

    FROM messages

    WHERE

    (
    sender=%s

    AND

    receiver=%s
    )

    OR

    (
    sender=%s

    AND

    receiver=%s
    )

    ORDER BY id
    """

    values = (
        current_user,
        selected_user,

        selected_user,
        current_user
    )

    cursor.execute(
        sql,
        values
    )

    messages = cursor.fetchall()

    # Users list
    sql = """
    SELECT

    username,

    status,

    last_seen

    FROM users

    WHERE username!=%s
    """

    cursor.execute(
        sql,
        (current_user,)
    )

    users = cursor.fetchall()

    return render_template(
        'chat.html',

        messages=messages,

        users=users,

        selected_user=selected_user,

        current_user=current_user
    )
# CLEAR CHAT
@app.route('/clear')
def clear_chat():

    if 'username' not in session:

        return redirect('/')

    cursor.execute(
        "DELETE FROM messages"
    )

    db.commit()

    return redirect(
        '/chat'
    )

@app.route('/delete/<int:message_id>')
def delete_message(message_id):

    if 'username' not in session:
        return redirect('/')

    username = session['username']

    sql = """
    DELETE FROM messages

    WHERE

    id=%s

    AND

    sender=%s
    """

    values = (
        message_id,
        username
    )

    cursor.execute(
        sql,
        values
    )

    db.commit()

    return redirect('/chat')
@app.route(
'/edit/<int:message_id>',
methods=['GET','POST']
)
def edit_message(message_id):

    if 'username' not in session:
        return redirect('/')

    username = session['username']

    if request.method == 'POST':

        new_message = request.form[
            'message'
        ]

        sql = """
        UPDATE messages

        SET message=%s

        WHERE

        id=%s

        AND

        sender=%s
        """

        values = (
            new_message,
            message_id,
            username
        )

        cursor.execute(
            sql,
            values
        )

        db.commit()

        return redirect('/chat')

    sql = """
    SELECT *

    FROM messages

    WHERE id=%s
    """

    cursor.execute(
        sql,
        (message_id,)
    )

    msg = cursor.fetchone()

    return render_template(
        'edit.html',
        msg=msg
    )

@app.route(
'/group',
methods=['GET','POST']
)
def group_chat():

    if 'username' not in session:
        return redirect('/')

    current_user = session[
        'username'
    ]

    if request.method == 'POST':

        message = request.form[
            'message'
        ]

        sql = """
        INSERT INTO messages(
        sender,
        receiver,
        message
        )

        VALUES(
        %s,
        %s,
        %s
        )
        """

        values = (
            current_user,
            'GROUP',
            message
        )

        cursor.execute(
            sql,
            values
        )

        db.commit()

    cursor.execute(
    """
    SELECT *

    FROM messages

    WHERE receiver='GROUP'

    ORDER BY created_at
    """
    )

    messages = cursor.fetchall()

    cursor.execute(
    """
    SELECT

    username,

    status,

    last_seen

    FROM users

    WHERE username!=%s
    """,

    (current_user,)
    )

    users = cursor.fetchall()

    return render_template(
        'chat.html',

        users=users,

        messages=messages,

        current_user=current_user,

        selected_user="GROUP CHAT"
    )
# LOGOUT
@app.route('/logout')
def logout():

    if 'username' in session:

        username = session[
            'username'
        ]

        cursor.execute(
        """
        UPDATE users

        SET

        status='Offline',

        last_seen=NOW()

        WHERE username=%s
        """,

        (username,)
        )

        db.commit()

    session.pop(
        'username',
        None
    )

    return redirect('/')


# RUN
if __name__ == '__main__':

    app.run(
        debug=True
    )
