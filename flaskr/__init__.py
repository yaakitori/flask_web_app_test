# 初期化処理を記入する
from flask import Flask
app = Flask(__name__)
import flaskr.main # main.pyをインポートしておく

# データベースを呼び出す
from flaskr import db
db.create_books_table()