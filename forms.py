from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class FriendForm(FlaskForm):
    name = StringField("이름", validators=[DataRequired()])
    email = StringField("이메일", validators=[DataRequired(), Email()])
    phone = StringField("전화번호", validators=[Optional()])
    submit = SubmitField("저장")