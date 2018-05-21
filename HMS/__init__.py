from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '82d4a58e933f7ae2463a9fc1486a15e5'

from HMS import routes
