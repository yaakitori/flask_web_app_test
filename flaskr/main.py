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
        # データを渡すこと自体と表示するかは別
        books.append(
            {
                "id": row[0],
                "title": row[1],
                "price": row[2],
                "arrival_day": row[3],
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

    # 何も入力されていr内項目がある場合はトップページに戻る
    if not title or not price or not arrival_day:
        return redirect(url_for("index"))

    # データベースのbooksのテーブルに登録したい
    con =sqlite3.connect(DATABASE)
    # (title, price, arrival_day) の3列にデータを追加する、と明記する
    con.execute(
        "INSERT INTO books (title, price, arrival_day) VALUES(?, ?, ?)", [title, price, arrival_day]
    ) # VALUESの値をそれぞれ指定
    con.commit()  # データベースに対する変更を確定（セーブ）するための命令
    con.close()
    return redirect(url_for('index')) # 処理が終わったらトップ画面を表示

# 削除ページを表示
@app.route('/delete')
def delete():

    # データベースと接続
    con = sqlite3.connect(DATABASE)
    # fetchall()で取得したすべてのデータをPythonのlistオブジェクトとして取得
    db_books = con.execute("SELECT * FROM books").fetchall()
    con.close()

    books = []
    # db_booksを辞書オブジェクトのリストに変換
    for row in db_books:
        books.append(
            {
                "id": row[0],
                "title": row[1],
                "price": row[2],
                "arrival_day": row[3],
            }
        )
    return render_template(
        'delete.html',
        books=books
    )

# データの削除
@app.route("/delete_books", methods=["POST"])
def delete_books():
    # どのデータを削除するか、チェックされたチェックボックスのvalueリストを受け取る
    # HTMLのname属性を指定する
    delete_ids = request.form.getlist("delete_ids")  # 同じname属性を持つフォーム要素（今回はチェックボックス）のvalueをリストとして受け取るためのメソッド

    # 何も選択されていない場合はトップページに戻る
    if not delete_ids:
        return redirect(url_for("index"))

    # データを削除
    con =sqlite3.connect(DATABASE)

    # SQLインジェクションを防ぐため、プレースホルダを使う
    # 処理の骨格だけを最初に渡し、後で値を分離して渡す。後から渡される値を「SQLの命令の一部」としてではなく、常に「ただの文字列や数値データ」として扱うことを保証してくれる
    # DELETE FROM books WHERE id IN (?, ?, ...) の形を動的に生成
    placeholders = ", ".join(["?" for _ in delete_ids])  # delete_titlesリストの要素数に合わせて、SQL文のプレースホルダ ? を必要な数だけカンマ区切りで生成
    sql = f"DELETE FROM books WHERE id IN ({placeholders})"
    con.execute(sql, delete_ids)

    con.commit()  # データベースに対する変更を確定（セーブ）するための命令
    con.close()

    return redirect(url_for("index"))  # 処理が終わったらトップ画面を表示