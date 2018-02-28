from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)

def _get_conditions():
    bundle = requests.get('https://api-v5-stu3.hspconsortium.org/DBMIBC/open/Condition?patient=cf-1518386133147')
    bundle = JSON.loads(bundle)
    entry = bundle.entry
    cons = [be.resource for be in bundle.entry] if bundle is not None and bundle.entry is not None else None
    if cons is not None and len(pres) > 0:
        return cons
    return None


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/birth-cert', methods=['GET', 'POST'])
def birth():
    return render_template('birthcert.html')

if __name__ == '__main__':
    app.run(debug=True)
