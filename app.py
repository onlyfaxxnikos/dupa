#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


# Database Connection
def get_db():
    return psycopg.connect(os.environ.get('DATABASE_URL'))


def init_db():
    """Initialize database with required tables"""
    if not os.environ.get('DATABASE_URL'):
        print("DATABASE_URL not set - skipping database initialization")
        return

    try:
        conn = get_db()
        cur = conn.cursor()

        # Users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                has_access BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_admin BOOLEAN DEFAULT FALSE
            )
        ''')

        # Generated documents table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS generated_documents (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                name VARCHAR(255),
                surname VARCHAR(255),
                pesel VARCHAR(11),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data JSON
            )
        ''')

        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")


# Serve HTML files
@app.route('/')
def index():
    return send_file('admin-login.html')


@app.route('/admin-login.html')
def admin_login_page():
    return send_file('admin-login.html')


@app.route('/login.html')
def login_page():
    return send_file('login.html')


@app.route('/gen.html')
def gen_page():
    return send_file('gen.html')


@app.route('/admin.html')
def admin_page():
    return send_file('admin.html')


# Routes
@app.route('/api/auth/create-user', methods=['POST'])
def create_user():
