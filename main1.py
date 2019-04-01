from flask import Flask, render_template, request, make_response,redirect
from orm import manage
from hashlib import sha1
import datetime
import tkinter
import tkinter.messagebox


app = Flask(__name__)
app.send_file_max_age_default = datetime.timedelta(seconds=1)
app.debug = True


@app.route("/")
def index():
    user = manage.selectuserbyid(request.cookies.get("id"))
    res = manage.selectarticle()
    return render_template("index.html", user=user, articlelist=res)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/registerUser", methods=["GET", "POST"])
def adduser():
    rname = request.form.get("username")
    rpwd = request.form.get("password")
    s1 = sha1()
    s1.update(rpwd.encode("utf8"))
    pwd = s1.hexdigest()
    try:
        manage.insertUser(rname, pwd)
        message = "注册成功，请登录"
        return render_template("login.html", message=message)
    except Exception as e:
        print(e)
        return redirect('/register')


@app.route("/checkAccount", methods=["GET", "POST"])
def check():
    loginname = request.form.get('username')
    loginpwd = request.form.get('password')
    s1 = sha1()
    s1.update(loginpwd.encode("utf8"))
    pwd = s1.hexdigest()
    res = manage.selectuser(loginname, pwd)
    if res is not None:
        # tkinter.messagebox.showinfo("提示", "登录成功")
        respon = make_response(redirect("/article/"+str(res.id)))
        respon.set_cookie("id", str(res.id))
        return respon
    else:
        # tkinter.messagebox.showerror("提示", "账号或密码不正确")
        message = "账号或密码不正确"
        return render_template("login.html", message=message)


@app.route("/article/<int:num>")
def publish(num):
    res = manage.selectmyself(num)
    user = manage.selectuserbyid(request.cookies.get("id"))
    return render_template("article.html", articlelist=res, user=user)
    # return "ffff"


@app.route("/aArticle")
def addart():
    user = manage.selectuserbyid(request.cookies.get("id"))
    return render_template("addArticle.html", user=user)


@app.route("/addArticle", methods=["GET", "POST"])
def addarticle():
    id = int(request.cookies.get("id"))
    title = request.form.get("title")
    content = request.form.get("content")
    manage.addarticle(title, content, id)
    return redirect('/article/'+str(id))


@app.route("/read/<int:num>")
def read(num):
    res = manage.selectone(num)
    getid = request.cookies.get("id")
    user = manage.selectuserbyid(request.cookies.get("id"))
    if getid is not None:
        flag = 1
    else:
        flag = 0
    return render_template("artcontent.html", article=res, flag=flag, user=user)


@app.route("/backArticle/<int:num>")
def back(num):
    if num == 0:
        return redirect("/")
    else:
        userid = request.cookies.get('id')
        return redirect('/article/'+str(userid))


@app.route("/modify/<int:num>")
def modify(num):
    res = manage.selectone(num)
    user = manage.selectuserbyid(request.cookies.get("id"))
    print(res.id)
    return render_template("modifyarticle.html", res=res,user=user)


@app.route("/modifycontent/<int:num>", methods=["GET", "POST"])
def modifycontent(num):
    id = request.cookies.get("id")
    title = request.form.get("title")
    content = request.form.get("content")
    manage.updatearticle(num, title, content)
    return redirect('/article/'+str(id))


@app.route("/deleteArticle/<int:num>")
def delete(num):
    id = request.cookies.get("id")
    manage.deletearticle(num)
    return redirect('/article/'+str(id))


@app.route("/quit")
def quit():
    res = make_response(redirect("/"))
    res.delete_cookie("id")
    return res


if __name__ == "__main__":
    app.run()
