from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from config import get_connection, mail
import datetime

user_bp = Blueprint("user", __name__)

# Secret serializer
serializer = URLSafeTimedSerializer("SECRET_KEY")

