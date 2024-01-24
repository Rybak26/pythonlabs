from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

class FeedbackForm(FlaskForm):
    name = StringField('Ваше ім\'я', validators=[DataRequired()])
    feedback = TextAreaField('Ваш відгук', validators=[DataRequired()])
    submit = SubmitField('Надіслати')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

def create_feedback_blueprint():
    feedback_blueprint = Blueprint('feedback', __name__)

    @feedback_blueprint.route('/', methods=['GET', 'POST'])
    def feedback():
        form = FeedbackForm()

        if form.validate_on_submit():
            name = form.name.data
            feedback_text = form.feedback.data
            feedback_entry = Feedback(name=name, feedback=feedback_text)
            db.session.add(feedback_entry)
            db.session.commit()
            flash('Ваш відгук був успішно збережений', 'success')
            return redirect(url_for('feedback.feedback'))

        feedback_entries = Feedback.query.all()
        return render_template('feedback.html', form=form, feedback_entries=feedback_entries)

    @feedback_blueprint.route('/delete/<int:id>', methods=['POST'])
    def delete_feedback(id):
        feedback_entry = Feedback.query.get_or_404(id)
        db.session.delete(feedback_entry)
        db.session.commit()
        flash('Відгук був успішно видалений', 'success')
        return redirect(url_for('feedback.feedback'))

    return feedback_blueprint

if __name__ == '__main__':
    app = create_app()
    feedback_blueprint = create_feedback_blueprint()
    app.register_blueprint(feedback_blueprint, url_prefix='/feedback') 
    app.run(debug=True)
