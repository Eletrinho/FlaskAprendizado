from app import app, login_manager, db
from flask import render_template, flash, redirect, url_for
from app.models.forms import LoginForm, RegisterForm, PostForm, FollowBtn
from app.models.table import Follow, User, Post
from flask_login import login_user, logout_user, current_user

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            flash("Logado com sucesso")
            return redirect(url_for("index"))
        else:
            flash("Login inválido")

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        regis = User(form.username.data, form.name.data, form.password.data, form.email.data)
        user_verifcation = User.query.filter_by(username=form.username.data).first()
        email_verification = User.query.filter_by(email=form.email.data).first()
        if user_verifcation and str(form.username.data) == str(user_verifcation.username):
            flash(f"Já existe um username registrado em: {form.username.data}")
        elif email_verification and str(form.email.data) == str(email_verification.email): 
            flash(f"Já existe um email registrado em: {form.email.data}")
        else:
            db.session.add(regis)
            db.session.commit()
            flash("Registrado com sucesso")
            return redirect(url_for("register"))
    return render_template('register.html', form=form)

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    postForm = PostForm()
    if postForm.validate_on_submit():
        postar = Post(postForm.content.data, current_user.id)
        db.session.add(postar)
        db.session.commit()

        return redirect(url_for("posts"))
    postagens = Post.query.all()
    postagens.reverse()
    return render_template("posts.html", postForm=postForm, postagens=postagens, users=User)

@app.route('/user/<usuario>', methods=['GET', 'POST'])
@app.route('/user/')
def user_page(usuario=None):
    verificacao = User.query.filter_by(username=usuario).first()
    if verificacao:
        postagens = Post.query.filter_by(user_id=verificacao.id).all()
        postagens.reverse()

        follow = FollowBtn()
        followers = Follow.query.filter_by(user_id=verificacao.id).all()
        followed = Follow.query.filter_by(user_id=verificacao.id, follower_id=current_user.id).first()

        if follow.validate_on_submit():
            followDb = Follow(verificacao.id, current_user.id)
            db.session.add(followDb)
            db.session.commit()
            return redirect(f"{usuario}")
        # fazer botão de unfollow
        return render_template('user.html', verificar=verificacao, postagens=postagens, users=User, follow=follow, followed=followed)
    else:
        return render_template('usererror.html')

@app.route('/delete')
def deleteaccount():
    usuario = User.query.filter_by(username=current_user.username).first()
    db.session.delete(usuario)
    db.session.commit()
    flash("Sua conta foi apagada com sucesso")
    return redirect(url_for("index"))