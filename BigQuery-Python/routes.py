# routes.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from config import Config
from bq_client import execute_query
from schema_validator import SchemaValidator

app = Flask(__name__)
app.config.from_object(Config)

# Instantiate the schema validator
schema_validator = SchemaValidator(Config.SCHEMA_PATH)

def get_user_role(username):
    """
    Server-side role validation: Verify the user's role from the authoritative source.
    This prevents forged session cookies from bypassing authorization checks.
    """
    user = Config.USERS.get(username)
    return user['role'] if user else None

def require_role(required_role):
    """
    Validate that the current session user has the required role by checking
    against the server-side user database, not just trusting the session cookie.
    """
    username = session.get('username')
    if not username:
        return False
    
    # Always verify role from authoritative source (Config.USERS), not from session
    actual_role = get_user_role(username)
    return actual_role == required_role

@app.route('/')
def home():
    if 'username' in session:
        # Verify role from server-side source, not session
        username = session['username']
        role = get_user_role(username)
        if role:
            return render_template('index.html', role=role, username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Config.USERS.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('home'))
        return "Invalid credentials!", 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

@app.route('/search', methods=['POST'])
def search_catalog():
    # Validate role server-side against authoritative source
    if not require_role('customer'):
        return "Unauthorized access!", 403

    catalog_type = request.form.get('catalog_type')
    owner = request.form.get('owner')

    # Validate the input
    # try:
    #     schema_validator.validate({"catalog_type": catalog_type, "owner": owner})
    # except ValueError as e:
    #     return jsonify({"error": str(e)}), 400
    
    #secure way
    # query = f"""
    # SELECT * FROM `your-project-id.dataset.catalog`
    # WHERE catalog_type = @catalog_type AND owner = @owner
    # """

    # job_config = bigquery.QueryJobConfig(
    #     query_parameters=[
    #         bigquery.ScalarQueryParameter("catalog_type", "STRING", catalog_type),
    #         bigquery.ScalarQueryParameter("owner", "STRING", owner),
    #     ]
    # )

    #insecure way 1
    query = f"""
    SELECT * FROM `your-project-id.dataset.catalog`
    WHERE catalog_type = {catalog_type} AND owner = {owner}
    """
 

    job_config = None

    try:
        catalog_results = execute_query(query, job_config)
        return jsonify(catalog_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update', methods=['POST'])
def update_catalog():
    # Validate role server-side against authoritative source
    if not require_role('admin'):
        return "Unauthorized access!", 403

    catalog_id = request.form.get('catalog_id')
    new_data = request.form.get('new_data')

    #secure coding
    query = f"""
    UPDATE `your-project-id.dataset.catalog`
    SET data_field = @new_data
    WHERE catalog_id = @catalog_id
    """



    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("new_data", "STRING", new_data),
            bigquery.ScalarQueryParameter("catalog_id", "STRING", catalog_id),
        ]
    )

    try:
        execute_query(query, job_config)
        return jsonify({"message": "Catalog updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
