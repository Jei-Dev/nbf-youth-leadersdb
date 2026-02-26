from flask import Flask
from modules.reg import reg_bp
from modules.inst import inst_bp
from modules.enrol import enrol_bp
from modules.graduate import grad_bp
from modules.auth import auth_bp
from config import init_mail

app = Flask(__name__)

# REQUIRED for sessions + token serializer
app.config["SECRET_KEY"] = "SUPER_SECRET_KEY_CHANGE_THIS"

# Initialize Mail
init_mail(app)

# Register blueprints
app.register_blueprint(reg_bp)
app.register_blueprint(inst_bp)
app.register_blueprint(enrol_bp)
app.register_blueprint(grad_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)