from flask import Flask, render_template, request, redirect, make_response
import datetime
from hashlib import sha1
from pymysqlhelper import MySqlHelper
from orm import model
app = Flask(__name__)
app.send_file_max_age_default = datetime.timedelta(seconds=1)


b1 = model.Book(1, "book1", 20)
b2 = model.Book(2, "book2", 20)
b3 = model.Book(3, "book3", 20)


@app.route('/')
# def index():
#     return render_template("index.html", booklist=["aaaa", "bbbb", "cccc"])
def login():
    user = request.cookies.get("name")
    return render_template("login.html", booklist=[b1, b2, b3], user=user)


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/list/<int:num>')
def list(num):
    user = request.cookies.get("name")
    return render_template('index.html', num=num,user=user)
# @app.route('/register_count')
# def register_count():
#     register_name = request.form.get('username')
#     register_pwd = request.form.get('password')
#     msql = MySqlHelper()
#     res = msql.select_one("select * from account where name = %s", (register_name,))
#     if res is None:
#         return render_template('register.html', message="账户已存在")
#     else:


@app.route('/show')
def show():
    user = request.cookies.get("name")
    return render_template('show.html', user=user)


@app.route('/check_login', methods=["GET", "POST"])
def checklogin():
    # if request.method == 'GET':
    #     print("get请求", request.args.get("password"))
    #     # return render_template("show.html")
    #     return "get"
    # else:
    #     print("post请求", request.form.get("password"))
    #     return "post"
    msql = MySqlHelper()
    name = request.form["username"]
    password = request.form["password"]
    s1 = sha1()
    s1.update(password.encode("utf8"))
    pwd = s1.hexdigest()
    # print(name,type(name), pwd)
    # conn = pymysql.Connect(host="localhost", user="root", password="123456",
    #                        database="goods", port=3306)
    # cur = conn.cursor()
    # sql = "select password from account where name =%s"
    res = msql.select_one("select * from account where name = %s", (name,))
    # cur.execute("select * from account where name = %s", (name,))
    # res = cur.fetchone()

    if res is None:
        print("账户不存在")
        return render_template("login.html", message="账户不存在")
    elif res[2] == pwd:
        print("登录成功")
        # return render_template("show.html")
        res = make_response(redirect('/show'))
        res.set_cookie("name", name)
        return res
    else:
        print("密码错误")
        return render_template("login.html", message="密码错误")
    # for i in res:
    #     print(i)
    # print(res)
    # print(res, type(res))
    # cur.close()
    # conn.close()
    # return res


@app.route("/quit")
def quit():
    res = make_response(redirect("/"))
    res.delete_cookie("name")
    return res


if __name__ == "__main__":
    app.run()
