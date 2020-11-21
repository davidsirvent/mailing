from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    @app.route('/')
    def index():        
        return "Index"

    return app
