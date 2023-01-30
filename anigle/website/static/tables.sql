create database anigle;

use anigle;

create table anime(
    aid int primary key auto_increment,
    title varchar(30) unique,
    progress varchar(10),
    genre varchar(30),
    studios varchar(30),
    no_ep int,
    aired date,
    about varchar(150),
    rating float default 0
);

create table viewer(
    vid int primary key auto_increment,
    fname varchar(20),
    lname varchar(20),
    age int,
    gender varchar(10),
    completed int,
    watching int,
    avg_rating float default 0 
);

create table va(
    vaid int primary key auto_increment,
    fname varchar(20),
    lname varchar(20),
    gender varchar(10),
    age int
);

create table casting(
    aid int,
    vaid int,
    charecter varchar(20),
    roles varchar(10),
    primary key(aid,vaid),
    foreign key(aid) references anime(aid) on delete cascade,
    foreign key(vaid) references va(vaid) on delete cascade
);

create table views(
    animid int,
    useid int,
    progress varchar(20),
    no_ep int default 0,
    rating float default 0,
    primary key(animid,useid),
    foreign key(animid) references anime(aid) on delete cascade,
    foreign key(useid) references viewer(vid) on delete cascade
);

create table login(
    username varchar(20) primary key,
    passwd varchar(10),
    userid int,
    foreign key(userid) references viewer(vid) on delete cascade
);

create trigger arate_i
after insert on views
for each row
update anime 
set rating=(select avg(rating) from views v where v.animid=new.animid)
where anime.aid=new.animid;

create trigger arate_u
after update on views
for each row
update anime 
set rating=(select avg(rating) from views v where v.animid=new.animid)
where anime.aid=new.animid;

create trigger arate_d
after delete on views
for each row
update anime 
set rating=(select avg(rating) from views v where v.animid=old.animid)
where anime.aid=old.animid;

create trigger urate_i
after insert on views
for each row
update viewer
set avg_rating=(select avg(rating) from views where useid=new.useid)
where viewer.vid=new.useid;

create trigger urate_u
after update on views
for each row
update viewer
set avg_rating=(select avg(rating) from views where useid=new.useid)
where viewer.vid=new.useid;

create trigger urate_d
after delete on views
for each row
update viewer
set avg_rating=(select avg(rating) from views where useid=old.useid)
where viewer.vid=old.useid;

create trigger log
after insert on viewer
for each row
insert into login values("temp",Null,new.vid);

create trigger compli ((#not working))
after insert on views
for each row
update views set no_ep=(select no_ep from anime where aid=new.animid)
where new.progress="completed";

create trigger compno
after update on views
for each row
update viewer w
set completed=(select count(animid) from views v where new.useid=v.useid and v.progress="completed")
where w.vid=new.useid;

create trigger compno_d
after delete on views
for each row
update viewer w
set completed=(select count(animid) from views v where old.useid=v.useid and v.progress="completed")
where w.vid=old.useid;

create trigger watno
after update on views
for each row
update viewer w
set watching=(select count(animid) from views v where new.useid=v.useid and v.progress="watching")
where w.vid=new.useid;

create trigger watno_i
after insert on views
for each row
update viewer w
set watching=(select count(animid) from views v where new.useid=v.useid and v.progress="watching")
where w.vid=new.useid;