from flask import Blueprint, jsonify, render_template, session, flash, redirect, url_for, request
from . import db
import json

views=Blueprint('views',__name__)

@views.route('/')
def home():
    session['fpcount']=0
    return render_template("anigle.html")

@views.route('/home',methods=['GET','POST'])
def uihome():
    if 'user' in session:
        if request.method=='POST':
            aname=request.form.get('search')#id
            cursor=db.cursor()
            cursor.execute(f'select aid,title from anime where title="{aname}"')
            alist=cursor.fetchall()
            b=False
            for i in alist:
                if aname in i:
                    b=True
                    k=i
            if b:
                session['aid']=k[0]
                return redirect(url_for('views.anime'))
            else:
                flash('anime not found!',category='error')
                return redirect(url_for('views.uihome'))
        return render_template('home.html')

    else:
        flash('session expired',category='error')
        return redirect(url_for('auth.login'))

@views.route('/profile')
def profile():
    if 'user' in session:
        usr=session['user']
        cursor=db.cursor()
        str2=f'where v.vid=l.userid and l.username="{usr}"'
        cursor.execute(f'select v.fname,v.lname,v.gender,v.completed,v.watching,v.avg_rating from viewer v,login l '+str2)
        session['prof']=cursor.fetchall()
        session['nc']=str(session['prof'][0][3])
        session['nw']=str(session['prof'][0][4])
        session['ar']=str(session['prof'][0][5])
        return render_template("profile.html")
    else:
        flash('session expired',category='error')
        return redirect(url_for('auth.login'))

@views.route('/watching')
def watching():
    if 'user' in session:
        cursor=db.cursor()
        str=session['user']
        cursor.execute(f'select userid from login where username="{str}"')
        uid=cursor.fetchone()
        userid=uid[0]
        session['userid']=userid
        cursor=db.cursor()
        try:
            str2=f'and v.useid="{userid}" and v.progress="watching"'
            cursor.execute(f'select a.title,v.no_ep,v.progress,v.rating from anime a,views v where a.aid=v.animid '+str2)
            compl_list=cursor.fetchall()
            session['clist']=compl_list
        except:
            compl_list=['empty']
            session['clist']=compl_list
            pass
        return render_template("watching.html")
    else:
        flash('session expired',category='error')
        return redirect(url_for('auth.login'))

@views.route('/completed')
def completed():
    if 'user' in session:
        cursor=db.cursor()
        str=session['user']
        cursor.execute(f'select userid from login where username="{str}"')
        uid=cursor.fetchone()
        userid=uid[0]
        session['userid']=userid
        cursor=db.cursor()
        try:
            str2=f'and v.useid="{userid}" and v.progress="completed"'
            cursor.execute(f'select a.title,v.no_ep,v.progress,v.rating from anime a,views v where a.aid=v.animid '+str2)
            compl_list=cursor.fetchall()
            session['clist']=compl_list
        except:
            compl_list=['empty']
            session['clist']=compl_list
            pass
        return render_template('completed.html')
    else:
        flash('session expired',category='error')
        return redirect(url_for('auth.login'))

@views.route('/anime',methods=['GET','POST'])
def anime():
    if request.method=='POST':
        if request.form['buttonname']=="add":
            cursor=db.cursor()
            aid=session['aid']
            str=session['user']
            cursor.execute(f'select userid from login where username="{str}"')
            uid=cursor.fetchone()
            userid=uid[0]
            cursor=db.cursor()
            cursor.execute(f'insert into views(animid,useid,progress) values({aid},{userid},"watching")')
            db.commit()
            flash('anime added to watching!',category='success')
        if request.form['buttonname']=="remove":
            cursor=db.cursor()
            aid=session['aid']
            str=session['user']
            cursor.execute(f'select userid from login where username="{str}"')
            uid=cursor.fetchone()
            userid=uid[0]
            cursor=db.cursor()
            cursor.execute(f'delete from views where animid={aid} and useid={userid}')
            db.commit()
            flash('anime removed from your list!',category='success')
        if request.form['buttonname']=="completed":
            cursor=db.cursor()
            aid=session['aid']
            str=session['user']
            cursor.execute(f'select userid from login where username="{str}"')
            uid=cursor.fetchone()
            userid=uid[0]
            cursor=db.cursor()
            cursor.execute(f'update views set progress="completed" where animid={aid} and useid={userid}')
            db.commit()
            flash('anime progress updated',category='success')
        if request.form['buttonname']=="rate":
            rate=request.form.get('rating',type=float)
            cursor=db.cursor()
            aid=session['aid']
            str=session['user']
            cursor.execute(f'select userid from login where username="{str}"')
            uid=cursor.fetchone()
            userid=uid[0]
            cursor=db.cursor()
            cursor.execute(f'update views set rating={rate} where animid={aid} and useid={userid}')
            db.commit()
            flash('anime progress updated',category='success')
        return redirect(url_for('views.anime'))
    if 'user' in session:
        aid=session['aid']
        cursor=db.cursor()
        cursor.execute(f'select a.aid,a.title,a.progress,a.genre,a.studios,a.no_ep,a.aired,a.about,a.rating from anime a where aid={aid}')
        als=cursor.fetchall()
        print(als)
        session['clist']=als
        cursor=db.cursor()
        str=session['user']
        cursor.execute(f'select userid from login where username="{str}"')
        uid=cursor.fetchone()
        userid=uid[0]
        cursor=db.cursor()
        cursor.execute(f'select * from views where animid={aid} and useid={userid} and progress="watching"')
        userdw=cursor.fetchall()
        if(len(userdw)==0):
            if 'userdw' in session:
                session.pop('userdw',None)
        else:
            session['userdw']=userdw
        cursor=db.cursor()
        cursor.execute(f'select * from views where animid={aid} and useid={userid} and progress="completed"')
        userdc=cursor.fetchall()
        if(len(userdc)==0):
            if 'userdc' in session:
                session.pop('userdc',None)
        else:
            session['userdc']=userdc
        return render_template('anime.html')
    else:
        flash('session expired',category='error')
        return redirect(url_for('auth.login'))

@views.route('/delw',methods=['POST'])
def delw():
    a = json.loads(request.data)
    print('here')
    aname=a['aname']
    cursor=db.cursor()
    cursor.execute(f'select aid from anime where title="{aname}"')
    b=cursor.fetchone()
    aid=b[0]
    cursor=db.cursor()
    str=session['user']
    cursor.execute(f'select userid from login where username="{str}"')
    uid=cursor.fetchone()
    userid=uid[0]
    cursor=db.cursor()
    cursor.execute(f'delete from views where animid={aid} and useid={userid}')
    db.commit()
    flash('removed from watching',category='success')
    return jsonify({})

@views.route('/admin')
def admin():
    return render_template('admin.html')