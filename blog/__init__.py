from flask import Flask
from blog.config import config
from blog.extensions import db,ckeditor,mail,moment,bootstrap

from blog.blueprints.auth import auth_bp
from blog.blueprints.blog import blog_bp
from blog.blueprints.admin import admin_bp

import os
import click

def create_app(config_name=None):
    if config_name ==None :
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask('blog')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_logging(app) #日志
    register_commands(app) #自定义shell命令
    register_errors(app)  #错误处理函数
    register_shell_context(app) #注册shell上下文处理函数
    register_template_context(app) #注册模板上下文处理函数

    return app

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

def register_extensions(app):
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

def register_logging(app):
    pass

def register_commands(app):
    @app.cli.command(help='生成虚拟数据 .')
    @click.option('--category',default=10,help='默认生成十种分类.')
    @click.option('--post',default=50,help='默认生成五十篇文章.')
    @click.option('--comment',default=500,help='默认生成五百条评论.')
    def forge (category,post,comment):
        from blog.fakes import fake_admin,fake_category,fake_comment,fake_post

        db.drop_all()
        db.create_all()

        click.echo('正在生成管理员..')
        fake_admin()

        click.echo('正在生成分类..')
        fake_category(category)

        click.echo('正在生成文章..')
        fake_post(post)

        click.echo('正在生成评论和回复..')
        fake_comment(comment)

        click.echo('虚拟数据已全部生成完毕..')

def register_errors(app):
    pass

def register_shell_context(app):
    @app.shell_context_processor
    def shell_context():
        return dict(db=db)

def register_template_context(app):
    pass


