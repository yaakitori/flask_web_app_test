from flaskr import app # __init__.pyのapp変数
from flask import render_template, request, redirect, url_for
import sqlite3
DATABASE = 'database.db'

@app.route('/') # ルーティング：WebアプリのトップのURLにリクエストが来たら下記の関数が呼ばれるように。Flask独自の書き方
def index(): # トップ画面にアクセスしたときに実行される

    # データベースと接続
    con = sqlite3.connect(DATABASE)
    # fetchall()で取得したすべてのデータをPythonのlistオブジェクトとして取得
    db_books = con.execute('SELECT * FROM books').fetchall()
    con.close()

    books = []
    # db_booksを辞書オブジェクトのリストに変換
    for row in db_books:
        books.append(
            {
                "title": row[0],
                "price": row[1],
                "arrival_day": row[2],
            }
        )
    return render_template(
        'index.html',
        books=books
    )  # index.html（画面）を表示させたい
    # 表示させたいデータはrender_templateの引数に設定（引数名は何でもいい）
    # 引数はいくつでも渡せる

@app.route('/form') # form関数 と /form URLを紐づける
def form():
    return render_template(
        'form.html'
    )

# 登録ボタンが押されたときに実行される関数
@app.route('/register', methods=['POST']) # /register URL かつ POSTリクエストのときに呼び出される
def register():
    # requestに送られてきたデータが入ってる
    title = request.form['title']
    price = request.form['price']
    arrival_day = request.form['arrival_day']
    # データベースのbooksのテーブルに登録したい

    con =sqlite3.connect(DATABASE)
    con.execute("INSERT INTO books VALUES(?, ?, ?)", [title, price, arrival_day]) # VALUESの値をそれぞれ指定
    con.commit()  # データベースに対する変更を確定（セーブ）するための命令
    con.close()
    return redirect(url_for('index')) # 処理が終わったらトップ画面を表示