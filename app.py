import os
from datetime import datetime
from urllib.parse import urlencode
import mysql.connector
import requests
from bcrypt import checkpw, gensalt, hashpw
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for, send_from_directory, g, make_response)
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')
app.secret_key = '1234'
staticfile=os.path.join('static', 'upload')
if not os.path.exists(staticfile):
    os.makedirs(staticfile)
video_folder = os.path.join(staticfile, 'Videos')
doc_folder = os.path.join(staticfile, 'Document')
thumb = os.path.join(staticfile, 'Thumbnail')
if not os.path.exists(video_folder):
    os.makedirs(video_folder)
if not os.path.exists(doc_folder):
    os.makedirs(doc_folder)
if not os.path.exists(thumb):
    os.makedirs(thumb)
UPLOAD_FOLDER_VIDEOS = 'static/upload/Videos'
UPLOAD_FOLDER_DOC = 'static/upload/Document'
Upload_Thumbnail = 'static/upload/Thumbnail'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER_VIDEOS'] = UPLOAD_FOLDER_VIDEOS
app.config['UPLOAD_FOLDER_DOC'] =  UPLOAD_FOLDER_DOC
app.config['Upload_Thumbnail'] = Upload_Thumbnail
app.config['ALLOWED_EXTENSIO'] = {'png', 'jpg', 'jpeg'}
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv'}
app.config['ALLOWED_EXTENSION'] = {'pdf', 'epub','docx','odt' ,'mobi', 'azw', 'azw3'}


cnx = mysql.connector.connect(user='root',
                              password='root',
                              host='localhost',
                              database='Elibrary')

cursor = cnx.cursor()
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
# in app.py


#Home 
@app.route('/')
def home():
    getall = "SELECT * FROM books"
    cursor.execute(getall)
    books = cursor.fetchall()
    is_logged_in = False
    if 'username' in session:
        is_logged_in = True
    return render_template('index.html', books=books, is_logged_in=is_logged_in)

    cnx.close()


# @app.before_request
# def before_request():
#     g.user = None
#     if 'username' in session:
#         cursor.execute("SELECT username FROM users WHERE id = %s", (session["id"],))
#         g.user = cursor.fetchone()

#About
@app.route('/about')
def about():
    cursor.execute("SELECT username FROM users WHERE id = %s", (session["id"],))
    useri = cursor.fetchone()
    return render_template('about.html', useri=useri)

@app.route('/login', methods=['GET', 'POST'])
#login Code Start
def login():
    is_logged_in = False
    if 'username' in session:
        is_logged_in = True
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (email, email))
        user = cursor.fetchone()
        if user:
            hashed_password = user[4].encode('utf-8')
            if checkpw(password, hashed_password):
                session['logged_in'] = True
                session['username'] = user[2]
                session['id']=user[0]
                return redirect(url_for('dashboard'))
        else:
            
            flash('Invalid email or password')
            return redirect('/login')
    else:
        return render_template('login.html', is_logged_in=is_logged_in)
    cnx.close()
#login code end


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']

    response = make_response(redirect('/'))
    response.delete_cookie('remember_token')
    flash('You were logged out')
    return response



#register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cursor = cnx.cursor()
        # Validate password
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'danger')
            return redirect(url_for('register'))
        elif not any(char.isdigit() for char in password):
            flash('Password must contain at least one number', 'danger')
            return redirect(url_for('register'))
        elif not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter', 'danger')
            return redirect(url_for('register'))
        elif not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter', 'danger')
            return redirect(url_for('register'))
        # Validate that the passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        else:
            # Check if the email already exists
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            email_exists = cursor.fetchone()
            if email_exists:
                flash('Email already exists', 'danger')
                return redirect(url_for('register'))
            # Check if the username already exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            username_exists = cursor.fetchone()
            if username_exists:
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))
            else:
                # Hash the password
                hashed_password = hashpw(password.encode('utf-8'), gensalt())
                # Insert the new user into the database
                query = 'INSERT INTO users (fullname, username, email, password) VALUES (%s, %s, %s, %s)'
                values = (name, username, email, hashed_password)                                  
                cursor.execute(query, values)
                cnx.commit()
                flash('You are now registered and can log in', 'success')
                session['logged_in'] = True
                return redirect(url_for('dashboard'))
    return render_template('register.html')
    cnx.close()
@app.route('/contact')
def contact():
    is_logged_in = False
    if 'username' in session:
        is_logged_in = True
    return render_template('contact.html', is_logged_in=is_logged_in)

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
    else:
        return redirect('/')
    return render_template("dashboard.html", books=books,year=datetime.now().year)
@app.route("/video")
def video():
    cursor.execute("SELECT * FROM videos")
    video=cursor.fetchall()
    return render_template("video.html", video=video, year=datetime.now().year)

@app.route('/upload/<path:filename>')
def send_thumbnail(filename):
    return send_from_directory('upload/Thumbnail', filename)
@app.route('/upload/<path:filename>')
def download_file(filename):
    return send_from_directory('upload/Document' , filename, as_attachment=True)
@app.route('/upload/<path:filename>')
def download_video(filename):
    return send_from_directory('upload/Videos' , filename, as_attachment=True)
@app.route('/read_book/<int:id>', methods=['GET', 'POST'])
def read_book(id):
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cursor.fetchone()
    ebook_path = '/static/upload/Document'+'/'+book[7]
    return render_template('read.html', book=book, ebook_path=ebook_path)

@app.route('/view_book/<id>', methods=['GET'])
def view_book(id):
    cursor = cnx.cursor()
    try:
        cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
        book = cursor.fetchone()
        if not book:
            raise ValueError("Book not found")
    # rest of the code
    except ValueError as e:
        return render_template("error.html", message=str(e))
    return render_template("book_detail.html", book=book)

@app.route('/view_video/<id>', methods=['GET'])
def view_video(id):
    cursor = cnx.cursor()
    try:
        cursor.execute("SELECT * FROM videos WHERE id = %s", (id,))
        video = cursor.fetchone()
        if not video:
            raise ValueError("video not found")
    except ValueError as e:
        return render_template("error.html", message=str(e))
    from urllib.parse import quote
    video_file_name = video[2]
    encoded_file_name = video_file_name.replace(" ", "%20")
    return render_template("video_detail.html", encoded_file_name=encoded_file_name, video=video)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                if user[5] == 1:
                    #user is an admin
                    hashed_password = user[4].encode('utf-8')
                    if checkpw(password, hashed_password):
                        session['logged_in'] = True
                        session['username'] = user[2]
                        session['is_admin'] = user[5]
                        return redirect('/admin/dashboard')
                else:
                    #user is not an admin
                    flash('You are not an admin')
                    return redirect('/admin')
            else:
                flash('Invalid email or password')
                return redirect('/admin')                                                                                                                       
    else:
        return render_template("admin.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM categories")
    total_categories = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM videos")
    total_video = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM users")
    recent_users = cursor.fetchall()
    cursor.execute("SELECT id FROM users")
    user=cursor.fetchall()
    cursor.execute("SELECT * FROM books")
    recent_books = cursor.fetchall()
    return render_template("admin_dashboard.html", total_books=total_books, total_video =total_video ,recent_books=recent_books,recent_users=recent_users,  total_users=total_users, total_categories=total_categories, user=user)

@app.route("/listbooks", methods=["GET", "POST"])
def listbooks():
    
    getall = "SELECT * FROM books"
    cursor.execute(getall)
    book_typ = cursor.fetchall()
    return render_template("listbooks.html", book=book_typ)
        
@app.route("/listvideos", methods=["GET", "POST"])
def listvideos():
    
    getall = "SELECT * FROM videos"
    cursor.execute(getall)
    video = cursor.fetchall()
    return render_template("listvideos.html", video=video)
        


@app.route("/add/books", methods=["GET", "POST"])
def add_books():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        category_id = request.form['category_id']
        file1 = request.files['file1']
        booktype = request.form['booktype']
        publisher = request.form['publisher']
        description = request.form['description']
        download_permission = request.form['download_permission']
        file = request.files['file']
        # validate input and handle file upload if necessary
        if not title or not author or not category_id or not booktype or not publisher or not description or not file1 or not file or not download_permission:
            flash('All fields are required!')
            return redirect('/add/books')
        # validate file type and size if necessary
        if file and allowed_files(file.filename) and (file1 and allowed_file1(file1.filename)):
            filename = secure_filenames(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_DOC'], filename))
            filename = secure_filename1(file1.filename)
            file1.save( os.path.join(app.config['Upload_Thumbnail'], filename))
        else:
            flash('Invalid file type!')
            return redirect('/add/books')
    # add book to database using cursor
        cursor.execute("INSERT INTO books (title, author, category_id, book_type, publisher, description, date_added, file,download_permission, thumbnail_url) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s)", (title, author, category_id, booktype, publisher, description, datetime.now(), file.filename, download_permission, file1.filename))
        cnx.commit()
        flash('Book added successfully!')
        return redirect("/add/books")
    else:
        # select all categories and book types
        getall = "SELECT * FROM books"
        cursor.execute(getall)
        book_typ = cursor.fetchall()
        categories_query = "SELECT id, name FROM categories"
        cursor.execute(categories_query)
        categories = cursor.fetchall()
        book_types_query = "SELECT id, name FROM book_types"
        cursor.execute(book_types_query)
        book_types = cursor.fetchall()
        
        return render_template("add_book.html", categories=categories, book_types=book_types, book=book_typ)
def allowed_files(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSION']

def secure_filenames(filename):
    return "".join(x for x in filename if x.isalnum() or x == '.')
def allowed_file1(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIO']

def secure_filename1(filename):
    return "".join(x for x in filename if x.isalnum() or x == '.')

@app.route("/edit/book/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        description = request.form['description']
        category_id = request.form['category_id']
        file1 = request.files["file1"]
        book_type = request.form['book_type']
        download_permission=request.form['download_permission']
        if file1 and allowed_file1(file1.filename): 
            filename = secure_filename1(file1.filename)
            file1.save( os.path.join(app.config['Upload_Thumbnail'], filename))
            cursor.execute("UPDATE books SET title=%s, author=%s, publisher=%s, description=%s, category_id=%s, book_type=%s, download_permission=%s,  thumbnail_url=%s WHERE id=%s", (title, author, publisher, description, category_id, book_type,download_permission, file1.filename, id))
            cnx.commit()
            flash('Book updated successfully!')
            return redirect("/add/books")
    else:
        cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
        book = cursor.fetchone()

        categories_query = "SELECT id, name FROM categories"
        cursor.execute(categories_query)
        categories = cursor.fetchall()
        book_types_query = "SELECT id, name FROM book_types"
        cursor.execute(book_types_query)
        book_types = cursor.fetchall()
        return render_template("edit_book.html", book=book, categories=categories, book_types=book_types)
def allowed_file1(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIO']

def secure_filename1(filename):
    return "".join(x for x in filename if x.isalnum() or x == '.')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/book-types", methods=["GET", "POST"])
def book_types():
    if request.method == 'POST':
        name = request.form.get("name")
        add_type_query = "INSERT INTO book_types (name) VALUES (%s)"
        cursor.execute(add_type_query, (name,))
        cnx.commit()
        flash("book type added successfully!")
        return redirect("/book-types")
    elif request.method == 'GET':
        getall = "SELECT * FROM book_types"
        cursor.execute(getall)
        book_typ = cursor.fetchall()
        return render_template("book-types.html", book_types=book_typ)
    else:
        return render_template("book-types.html", book_types=book_typ)


@app.route("/delete-book-type/<int:id>", methods=["GET", "POST"])
def delete_book_type(id):
    delete_type_query = "DELETE FROM book_types WHERE id = %s"
    cursor.execute(delete_type_query, (id,))
    cnx.commit()
    flash("book type deleted successfully!")
    return redirect("/book-types")

@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == 'POST':
        name = request.form.get("name")
        add_type_query = "INSERT INTO categories (name) VALUES (%s)"
        cursor.execute(add_type_query, (name,))
        cnx.commit()
        flash("Category added successfully!")
        return redirect("/categories")
    elif request.method == 'GET':
        getall = "SELECT * FROM categories"
        cursor.execute(getall)
        catego = cursor.fetchall()
        return render_template("categories.html", categories=catego)
    else:
        return render_template("categories.html", categories=catego)


@app.route("/delete-categories/<int:id>", methods=["GET", "POST"])
def delete_categories(id):
    delete_type_query = "DELETE FROM categories WHERE id = %s"
    cursor.execute(delete_type_query, (id,))
    cnx.commit()
    flash("category deleted successfully!")
    return redirect("/categories")
@app.route("/add/video", methods=["GET", "POST"])
def add_video():
    if request.method == "POST":
        title = request.form["title"]
        category_id = request.form["category_id"]
        description = request.form["description"]
        file1=request.files['file1']
        file = request.files['file']
        download_permission = request.form['download_permission']
        if file and allowed_file(file.filename) and file1 and allowed_file1(file1.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename))
            filename = secure_filename1(file1.filename)
            file1.save( os.path.join(app.config['Upload_Thumbnail'], filename))
            cursor.execute("INSERT INTO videos (title, video_url, category_id, description, download_permission, thumbnail_url) VALUES (%s, %s, %s, %s, %s, %s)", (title, file.filename, category_id, description, download_permission, file1.filename))
            cnx.commit()
            flash("Video added successfully!")
            return redirect("/add/video")
        else:
            flash("Invalid file type. Only mp4, avi, mkv are allowed.")
            return redirect("/add/video")
    else:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        getall = "SELECT * FROM videos"
        cursor.execute(getall)
        vid_typ = cursor.fetchall()
        return render_template("add_video.html", video=vid_typ, categories=categories)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def secure_filename(filename):
    return "".join(x for x in filename if x.isalnum() or x == '.')
def allowed_file1(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIO']

def secure_filename1(filename):
    return "".join(x for x in filename if x.isalnum() or x == '.')

@app.route("/edit/video/<int:id>", methods=["GET", "POST"])
def edit_video(id):
    cursor.execute("SELECT * FROM videos WHERE id = %s", (id,))
    video = cursor.fetchone()
    if request.method == "POST":
        title = request.form["title"]
        category_id = request.form["category_id"]
        description = request.form["description"]
        file1 = request.files["file1"]
        download_permission=request.form['download_permission']
        if file1 and allowed_file1(file1.filename): 
            filename = secure_filename1(file1.filename)
            file1.save( os.path.join(app.config['Upload_Thumbnail'], filename))
            cursor.execute("UPDATE videos SET title=%s, category_id=%s, description=%s, download_permission=%s, thumbnail_url=%s WHERE id=%s", (title, category_id,description,download_permission,file1.filename, id))
            cnx.commit()
            flash("Video updated successfully!")
            return redirect("/add/video")
    else:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return render_template("edit_video.html", video=video, categories=categories)
def allowed_file1(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIO']

def secure_filename1(filename):
    return "".join(x for x in filename if x.isalnum() or x == '.')
@app.route('/report')
def report():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('report.html', books=books)
@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    if request.method == "POST":
        password = request.form['password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # check if current password is correct
        cursor.execute("SELECT password FROM users WHERE id = %s", (session['id'],))
        current_password = cursor.fetchone()[0]
        if not checkpw(password.encode('utf-8'), current_password.encode('utf-8')):
            flash("Current password is incorrect", "danger")
            return redirect(url_for('changepassword'))
        # elif checkpw(password.encode('utf-8'), current_password.encode('utf-8')) == checkpw(password.encode('utf-8'), current_password.encode('utf-8')):
        #     flash("New Password cant Be the same with current password")
        #     redirect(url_for('changepassword'))

        # Validate new password
        if len(new_password) < 8:
            flash('Password must be at least 8 characters long', 'danger')
            return redirect(url_for('changepassword'))
        elif not any(char.isdigit() for char in new_password):
            flash('Password must contain at least one number', 'danger')
            return redirect(url_for('changepassword'))
        elif not any(char.isupper() for char in new_password):
            flash('Password must contain at least one uppercase letter', 'danger')
            return redirect(url_for('changepassword'))
        elif not any(char.islower() for char in new_password):
            flash('Password must contain at least one lowercase letter', 'danger')
            return redirect(url_for('changepassword'))

        # check if new password and confirm password match
        if new_password != confirm_password:
            flash("New password and confirm password do not match", "danger")
            return redirect(url_for('changepassword'))
        elif new_password == password:
            flash("New Password cant Be the same with current password")
            return redirect(url_for('changepassword'))
        else:
        # update the password in the database
            hashed_password = hashpw(new_password.encode('utf-8'), gensalt())
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, session['id']))
            cnx.commit()
            flash("Password successfully updated", "success")
            return redirect(url_for('profile'))
    else:
        cursor.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
        current_user = cursor.fetchone()
        return render_template("changepassword.html", current_user=current_user)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # if 'id' not in session:
    #     return redirect(url_for('login'))
    if request.method == "GET":
        cursor.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
        current_user = cursor.fetchone()
        return render_template("profile.html", current_user=current_user)

    elif request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        email_exists = cursor.fetchone()
        if email_exists:
            flash('Email already exists', 'danger')
            return redirect(url_for('profile'))
        # Check if the username already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        username_exists = cursor.fetchone()
        if username_exists:
                flash('Username already exists', 'danger')
                return redirect(url_for('profile'))
        cursor.execute("UPDATE users SET fullname=%s, username=%s, email=%s WHERE id=%s", (name, username, email, session['id']))
        cnx.commit()
        flash("User Details Updated Successfully")  
        return redirect(url_for('profile'))  
@app.route("/admin/logout")
def admin_logout():
    return redirect(url_for("admin"))
if __name__ == '__main__':
    app.debug = True
    app.run()

