from flask import Flask
from modules.reg import reg_bp
from modules.inst import inst_bp
from modules.enrol import enrol_bp
from modules.graduate import grad_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(reg_bp)
# Settings. instituitions and course blueprints
app.register_blueprint(inst_bp)
# enrollment blueprints
app.register_blueprint(enrol_bp)
# graduate blueprint
app.register_blueprint(grad_bp)

if __name__ == "__main__":
    app.run(debug=True)
