from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from app.models import User, Map, Grenade

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', 
                          validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', 
                            validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username): #self - сама форма, username - поле в этой форме
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email уже используется.')
        
class VideoForm(FlaskForm):
    """Форма добавления видео"""
    title = StringField('Название видео', 
                       validators=[DataRequired(), Length(max=200)])
    
    description = TextAreaField('Описание', 
                               validators=[Length(max=500)],
                               render_kw={"rows": 4})
    
    video_url = StringField('Ссылка на YouTube видео', 
                           validators=[DataRequired(), URL()])
    
    map_id = SelectField('Карта', 
                        coerce=int,
                        validators=[DataRequired()])
    
    grenade_id = SelectField('Тип гранаты', 
                            coerce=int,
                            validators=[DataRequired()])
    
    submit = SubmitField('Добавить видео')
    
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        # Динамически заполняем выбор карт и гранат из базы данных
        self.map_id.choices = [(map.id, map.display_name) for map in Map.query.order_by('display_name').all()]
        self.grenade_id.choices = [(grenade.id, grenade.display_name) for grenade in Grenade.query.order_by('display_name').all()]

class EditVideoForm(FlaskForm):
    """Форма редактирования видео"""
    title = StringField('Название видео', 
                       validators=[DataRequired(), Length(max=200)])
    
    description = TextAreaField('Описание', 
                               validators=[Length(max=500)],
                               render_kw={"rows": 4})
    
    video_url = StringField('Ссылка на YouTube видео', 
                           validators=[DataRequired(), URL()],
                           render_kw={"placeholder": "https://www.youtube.com/watch?v=..."})
    
    map_id = SelectField('Карта', 
                        coerce=int,
                        validators=[DataRequired()])
    
    grenade_id = SelectField('Тип гранаты', 
                            coerce=int,
                            validators=[DataRequired()])
    
    submit = SubmitField('Сохранить изменения')
    
    def __init__(self, *args, **kwargs):
        super(EditVideoForm, self).__init__(*args, **kwargs)
        # Динамически заполняем выбор карт и гранат из базы данных
        self.map_id.choices = [(map.id, map.display_name) for map in Map.query.order_by('display_name').all()]
        self.grenade_id.choices = [(grenade.id, grenade.display_name) for grenade in Grenade.query.order_by('display_name').all()]