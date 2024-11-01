from flask import Flask, jsonify, request, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from functools import wraps
import jwt
import datetime
import os

# =============================================
# TASK 1: CONFIGURATION AND SETUP
# =============================================
# Application Configuration
app = Flask(__name__)

# Database Configuration
app.config['MYSQL_USER'] = 'flaskuser'
app.config['MYSQL_PASSWORD'] = 'flaskpassword'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'flask_api_db'

# JWT Configuration
app.config['SECRET_KEY'] = 'secret'

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

mysql = MySQL(app)

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# =============================================
# TASK 2: ERROR HANDLING
# =============================================
def error_response(status_code, message):
    """
    Creates a standardized error response format
    Args:
        status_code (int): HTTP status code
        message (str): Error message
    Returns:
        JSON response with error details
    """
    response = jsonify({
        "error": {
            "code": status_code,
            "message": message
        }
    })
    response.status_code = status_code
    return response

def allowed_file(filename):
    """
    Validates file extension against allowed types
    Args:
        filename (str): Name of the uploaded file
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =============================================
# TASK 3: AUTHENTICATION
# =============================================
def token_required(f):
    """
    Decorator for protecting routes that require authentication
    Args:
        f (function): The route function to protect
    Returns:
        decorated function that checks for valid JWT token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return error_response(401, 'Token is missing')
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Get current user from database
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM midterm_database WHERE username = %s", (data['username'],))
            current_user = cur.fetchone()
            cur.close()
            
            if not current_user:
                return error_response(401, 'Invalid token')
                
        except Exception as e:
            return error_response(401, 'Invalid token')
            
        return f(current_user, *args, **kwargs)
    
    return decorated

# Database setup route
@app.route('/create_table')
def create_table():
    """
    Initializes the database table and populates it with sample users
    Returns:
        200: Table created successfully
        500: Database error
    """
    try:
        cursor = mysql.connection.cursor()
        
        # Create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS midterm_database(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(20) UNIQUE,
                password VARCHAR(255)
            )
        """)
        
        # Insert sample users
        sample_users = [
            ('emmanuel_montoya', 'em12345'),
            ('renzo_salosagcol', 'rs12345'),
            ('anthony_weathersby', 'aw12345'),
            ('alice_johnson', 'aj12345'),
            ('brian_smith', 'bs12345'),
            ('carla_brown', 'cb12345'),
            ('david_taylor', 'dt12345'),
            ('emily_davis', 'ed12345'),
            ('frank_wilson', 'fw12345'),
            ('grace_martinez', 'gm12345')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM midterm_database")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.executemany(
                "INSERT INTO midterm_database (username, password) VALUES (%s, %s)",
                sample_users
            )
            
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Table created and populated successfully"}), 200
        
    except Exception as e:
        return error_response(500, str(e))

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticates user and provides JWT token
    Required: Basic Authentication header with username and password
    Returns:
        200: JWT token
        401: Invalid credentials
    """
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return error_response(401, 'Login required')
        
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM midterm_database WHERE username = %s AND password = %s",
                  (auth.username, auth.password))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        return error_response(401, 'Invalid credentials')
        
    token = jwt.encode({
        'username': auth.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({'token': token})

# =============================================
# TASK 4: FILE HANDLING
# =============================================
@app.route('/admin/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    """
    Handles file uploads with the following validations:
    - Validates file presence
    - Checks file type against allowed extensions
    - Enforces maximum file size (16MB)
    - Stores files securely in uploads directory
    
    Returns:
        200: File uploaded successfully
        400: Invalid file or file type
        401: Invalid authentication
    """
    if 'file' not in request.files:
        return error_response(400, 'No file part')
        
    file = request.files['file']
    
    if file.filename == '':
        return error_response(400, 'No selected file')
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename
        })
    
    return error_response(400, 'File type not allowed')

# =============================================
# TASK 5: PUBLIC ROUTES
# =============================================
@app.route('/public/items', methods=['GET'])
def get_public_items():
    """
    Public endpoint that doesn't require authentication
    Returns a list of public items available in the system
    
    Returns:
        200: List of public items
    """
    items = [
        {"id": 1, "name": "Public Item 1", "description": "This is a public item"},
        {"id": 2, "name": "Public Item 2", "description": "This is another public item"}
    ]
    return jsonify({"items": items})

# =============================================
# TASK 3: PROTECTED ROUTES
# =============================================
@app.route('/admin/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Protected route that returns the current user's profile
    Requires valid JWT token in Authorization header
    
    Returns:
        200: User profile information
        401: Invalid or missing token
    """
    return jsonify({
        "username": current_user[1],
        "message": "This is a protected route"
    })

# =============================================
# TASK 6: CRUD SERVICES
# =============================================
# User Management Operations
@app.route('/users', methods=['POST'])
@token_required
def create_user(current_user):
    """
    Creates a new user in the system
    Required JSON payload:
    {
        "username": "string",
        "password": "string"
    }
    Returns:
        201: User created successfully
        400: Invalid input
        409: Username already exists
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return error_response(400, 'Username and password are required')
            
        cursor = mysql.connection.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT * FROM midterm_database WHERE username = %s", (data['username'],))
        if cursor.fetchone():
            cursor.close()
            return error_response(409, 'Username already exists')
            
        # Insert new user
        cursor.execute(
            "INSERT INTO midterm_database (username, password) VALUES (%s, %s)",
            (data['username'], data['password'])
        )
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({
            "message": "User created successfully",
            "username": data['username']
        }), 201
        
    except Exception as e:
        return error_response(500, str(e))

@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    Retrieves all users in the system
    
    Returns:
        200: List of all users
        500: Server error
    """
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, username FROM midterm_database")
        users = cursor.fetchall()
        cursor.close()
        
        user_list = []
        for user in users:
            user_list.append({
                "id": user[0],
                "username": user[1]
            })
        
        return jsonify({"users": user_list})
        
    except Exception as e:
        return error_response(500, str(e))

@app.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """
    Retrieves a specific user by ID
    
    Args:
        user_id: The ID of the user to retrieve
    Returns:
        200: User details
        404: User not found
    """
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, username FROM midterm_database WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            return error_response(404, 'User not found')
            
        return jsonify({
            "id": user[0],
            "username": user[1]
        })
        
    except Exception as e:
        return error_response(500, str(e))

@app.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """
    Updates an existing user's information
    Required JSON payload:
    {
        "username": "string" (optional),
        "password": "string" (optional)
    }
    Returns:
        200: User updated successfully
        400: Invalid input
        404: User not found
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response(400, 'No data provided')
            
        cursor = mysql.connection.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM midterm_database WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            return error_response(404, 'User not found')
            
        # Update user information
        update_query = "UPDATE midterm_database SET "
        update_params = []
        
        if 'username' in data:
            update_query += "username = %s"
            update_params.append(data['username'])
            
        if 'password' in data:
            if 'username' in data:
                update_query += ", "
            update_query += "password = %s"
            update_params.append(data['password'])
            
        update_query += " WHERE id = %s"
        update_params.append(user_id)
        
        cursor.execute(update_query, tuple(update_params))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "User updated successfully"})
        
    except Exception as e:
        return error_response(500, str(e))

@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    """
    Deletes a user from the system
    
    Args:
        user_id: The ID of the user to delete
    Returns:
        200: User deleted successfully
        404: User not found
    """
    try:
        cursor = mysql.connection.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM midterm_database WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            return error_response(404, 'User not found')
            
        # Delete user
        cursor.execute("DELETE FROM midterm_database WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "User deleted successfully"})
        
    except Exception as e:
        return error_response(500, str(e))

# File CRUD Operations
@app.route('/files', methods=['GET'])
@token_required
def get_all_files(current_user):
    """
    Lists all files in the upload directory
    Returns file metadata including name, size, and upload date
    
    Returns:
        200: List of file information
        500: Server error
    """
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            files.append({
                "filename": filename,
                "size": os.path.getsize(file_path),
                "uploaded_at": datetime.datetime.fromtimestamp(
                    os.path.getctime(file_path)
                ).strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({"files": files})
        
    except Exception as e:
        return error_response(500, str(e))

@app.route('/files/<filename>', methods=['GET'])
@token_required
def get_file(current_user, filename):
    """
    Downloads a specific file
    
    Args:
        filename: Name of the file to download
        Returns:
        200: File download
        404: File not found
    """
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except Exception as e:
        return error_response(404, 'File not found')

@app.route('/files/<filename>', methods=['DELETE'])
@token_required
def delete_file(current_user, filename):
    """
    Deletes a specific file from the upload directory
    
    Args:
        filename: Name of the file to delete
    Returns:
        200: File deleted successfully
        404: File not found
    """
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return error_response(404, 'File not found')
            
        os.remove(file_path)
        return jsonify({"message": "File deleted successfully"})
        
    except Exception as e:
        return error_response(500, str(e))

# =============================================
# TASK 2: ERROR HANDLERS
# =============================================
"""
Error Handler Overview:
400 - Bad Request: Invalid input or malformed request
401 - Unauthorized: Missing or invalid authentication
403 - Forbidden: Valid auth but insufficient permissions
404 - Not Found: Resource doesn't exist
406 - Not Acceptable: Invalid content negotiation
415 - Unsupported Media: Invalid content type
429 - Too Many Requests: Rate limit exceeded
"""

@app.errorhandler(400)
def bad_request_error(error):
    """
    Handles Bad Request errors
    Returns standardized error response for invalid requests
    """
    return error_response(400, "Bad Request")

@app.errorhandler(401)
def unauthorized_error(error):
    """
    Handles Unauthorized errors
    Returns standardized error response for authentication failures
    """
    return error_response(401, "Unauthorized")

@app.errorhandler(403)
def forbidden_error(error):
    """
    Handles Forbidden errors
    Returns standardized error response for permission-related failures
    """
    return error_response(403, "Forbidden")

@app.errorhandler(404)
def not_found_error(error):
    """
    Handles Not Found errors
    Returns standardized error response for missing resources
    """
    return error_response(404, "Page Not Found")

@app.errorhandler(406)
def not_acceptable_error(error):
    """
    Handles Not Acceptable errors
    Returns standardized error response for content negotiation failures
    """
    return error_response(406, "Not Acceptable")

@app.errorhandler(415)
def unsupported_media_error(error):
    """
    Handles Unsupported Media Type errors
    Returns standardized error response for invalid content types
    """
    return error_response(415, "Unsupported Media Type")

@app.errorhandler(429)
def too_many_requests_error(error):
    """
    Handles Too Many Requests errors
    Returns standardized error response for rate limiting
    """
    return error_response(429, "Too Many Requests")

if __name__ == "__main__":
    app.run(debug=True, port=5001)