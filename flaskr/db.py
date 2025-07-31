# データベース用
import sqlite3

DATABASE = "database.db" # データベース名は関数として扱う

def create_books_table():
    con = sqlite3.connect(DATABASE) # データベースアクセス用のコネクションオブジェクトの作成
    # id INTEGER PRIMARY KEY AUTOINCREMENTを追加。これにより、データが追加されるたびに、重複しないユニークな番号が自動で割り振られます
    con.execute(
        "CREATE TABLE  IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price INTEGER, arrival_day TEXT)"
    )
    con.close() # SQL文を文字列で指定
    con.close() # データベースとの接続を閉じる