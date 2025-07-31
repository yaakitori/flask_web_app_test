# データベース用
import sqlite3

DATABASE = "database.db" # データベース名は関数として扱う

def create_books_table():
    con = sqlite3.connect(DATABASE) # データベースアクセス用のコネクションオブジェクトの作成
    con.execute("CREATE TABLE  IF NOT EXISTS books (title, price, arrival_day)") # SQL文を文字列で指定
    con.close() # データベースとの接続を閉じる