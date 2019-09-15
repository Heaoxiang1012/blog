from blog.extensions import db
from blog.models import Admin,Category,Post,Comment
from faker import Faker
import random

fake =Faker('zh_CN')

def fake_admin():
    admin = Admin(
        username = '管理员' ,
        blog_title = '博客' ,
        blog_sub_title = '这里还没有什么简介',
        name = '何翱翔',
        about = '这是我的一个flask练习小项目！'
    )
    admin.password_hash='123456'
    db.session.add(admin)
    db.session.commit()

def fake_category(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category=Category(name=fake.word())
        db.session.add(category)

        try :
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_post(count=50):
    for i in range(count):
        post=Post(
            title=fake.sentence(),
            body = fake.text(200),
            category = Category.query.get(random.randint(1,Category.query.count())),
            timestamp = fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()

def fake_comment(count=500):
    for i in range(count):
        comment = Comment(
            author = fake.name(),
            email = fake.email(),
            site= fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True ,
            post = Post.query.get(random.randint(1,Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count*0.1)
    #未审核
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        comment = Comment(
            author = '何翱翔',
            email = '921269066@qq.com',
            site = 'www.hax.com',
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            from_admin = True,
            reviewed = True,
            post = Post.query.get(random.randint(1,Post.query.count()))
        )
        db.session.add(comment)

    db.session.commit()
    #回复
    for i in range(salt):
        comment=Comment(
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True ,
            replied = Comment.query.get(random.randint(1,Comment.query.count())),
            post = Post.query.get(random.randint(1,Post.query.count())),
        )
        db.session.add(comment)

    db.session.commit()
