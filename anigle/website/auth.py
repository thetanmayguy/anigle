from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user
from . import db

auth=Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form.get('username')
        passwd=request.form.get('passwd')

        #check if admin:-
        if uname=="admin" and passwd=="admin@123":
            session['user']=uname
            return render_template("admin.html")

        #sql query to check if user has an account (user = query)->user used in login_user
            #if exists, does passwords match?
                #flash('logged in successfully!',category='success')
                #login_user(user, remember=True)
                #redirect to ui
            #else:
                #flash('password incorrect!',category='error')
        #else:
            #flash('imposter!, sign up if you want to be one of us!',category='error')

        cursor=db.cursor()
        cursor.execute('select username from login')
        ulist=cursor.fetchall()
        b=False
        for i in ulist:
            if uname in i:
                b=True
        if b!=True:
            flash('imposter!, sign up if you want to be one of us!',category='error')
            return render_template("login.html",text="hello")
        
        cursor=db.cursor()
        cursor.execute(f'select passwd from login where username="{uname}"')
        ls=cursor.fetchall()
        for i in ls:
            if passwd in i:
                flash('logged in successfully!',category='success')
                session['user']=uname
                session['fpcount']=0
                #login_user(a)
                return redirect(url_for('views.uihome'))
                # if render template is used, redirecting does'nt take place, 
                # if back button clicked-> goes back to home after logout
            else:
                flash('imposter!, incorrect password',category='error')

    return render_template("login.html",text="hello")

@auth.route('/logout')
#@login_required #page accessible only if logged in
def logout():
    session.pop('user',None)
    #logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        uname=request.form.get('uname')
        gen=request.form.get('gender')
        passwd=request.form.get('passwd')
        cpasswd=request.form.get('c_passwd')
        
        #sql query to check if user already has an account
            #flash('username already taken!',category='error')
        cursor=db.cursor()
        cursor.execute('select username from login')
        username_list=cursor.fetchall()
        for u in username_list:
            if uname in u:
                flash('username already taken!',category='error')
                return render_template("signup.html")
        
        if len(fname)==0:
            flash('first name cannot be empty',category='error')
        elif len(fname)>20:
            flash('first name too long',category='error')
        elif len(lname)>20:
            flash('last name too long',category='error')
        elif len(uname)==0:
            flash('username cannot be empty',category='error')
        elif len(uname)>20:
            flash('username too long',category='error')
        elif len(gen)>6:
            flash('invalid gender',category='error')
        elif len(passwd)>10:
            flash('password too long',category='error')
        elif len(passwd)==0:
            flash('password cannot be empty',category='error')
        elif passwd!=cpasswd:
            flash('passwords don\'t match',category='error')
        else:
            #db operations
            cursor.execute(f'insert into viewer(fname,lname,age,gender) values("{fname}","{lname}",20,"{gen}")')
            cursor.execute(f'update login set username="{uname}",passwd="{passwd}" where username="temp"')
            db.commit()
            flash('account successfully created!',category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html")

@auth.route('/forgot_passwd')
def forgpass():
    session['fpcount']+=1
    if session['fpcount']<3:
        return render_template('forgot_passwd_lol.html')
    else:
        return render_template('forgot_passwd.html')

@auth.route('/anime_add',methods=['GET','POST'])
def addnime():
    if request.method=='POST':
        title=request.form.get('title')
        progress=request.form.get('progress')
        genre=request.form.get('genre')
        studios=request.form.get('studios')
        about=request.form.get('about')
        title=request.form.get('title')
        sdate=request.form.get('aired')
        noep=request.form.get('noep',type=int)
        cursor=db.cursor()
        cursor.execute(f'select aid from anime where title="{title}"')
        if len(cursor.fetchall())>0:
            flash('anime already exists',category='error')
            return redirect(url_for('views.admin'))
        else:
            cursor=db.cursor()
            str=f'"{progress}","{genre}","{studios}",{noep},"{sdate}","{about}")'
            cursor.execute(f'insert into anime(title,progress,genre,studios,no_ep,aired,about) values("{title}",'+str)
            db.commit()
            flash('anime added',category='success')
            return redirect(url_for('views.admin'))

    return render_template("addnime.html")

@auth.route('/anime_del',methods=['GET','POST'])
def delnime():
    if request.method=='POST':
        title=request.form.get('title')
        cursor=db.cursor()
        cursor.execute(f'select aid from anime where title="{title}"')
        if len(cursor.fetchall())>0:
            cursor=db.cursor()
            cursor.execute(f'delete from anime where title="{title}"')
            db.commit()
            flash('anime deleted',category='success')
            return redirect(url_for('views.admin'))
        else:     
            flash('anime does not exist',category='error')
            return redirect(url_for('views.admin'))

    return render_template("delnime.html")

@auth.route('/anime_up',methods=['GET','POST'])
def upanime():
    if request.method=='POST':
        title=request.form.get('title')
        cursor=db.cursor()
        cursor.execute(f'select aid from anime where title="{title}"')
        if len(cursor.fetchall())>0:
            cursor=db.cursor()
            cursor.execute(f'select * from anime where title="{title}"')
            session['upd_pars']=cursor.fetchone()
            return redirect(url_for('auth.upnime'))
        else:
            flash('anime does not exist',category='error')
            return redirect(url_for('views.admin'))
    return render_template('updanim.html')

@auth.route('/anime_update',methods=['GET','POST'])
def upnime():
    if request.method=='POST':
        progress=request.form.get('progress')
        print(progress)
        genre=request.form.get('genre')
        print(genre)
        studios=request.form.get('studios')
        print(studios)
        about=request.form.get('about')
        print(about)
        title=session['upd_pars'][1]
        print(title)
        sdate=request.form.get('aired')
        print(sdate)
        noep=request.form.get('noep',type=int)
        print(noep)
        cursor=db.cursor()
        str=f',aired="{sdate}",no_ep={noep} where title="{title}"'
        cursor.execute(f'update anime set progress="{progress}",genre="{genre}",studios="{studios}",about="{about}"'+str)
        db.commit()
        flash('anime updated successfully',category='success')
        return redirect(url_for('views.admin'))

    return render_template('upnime.html')