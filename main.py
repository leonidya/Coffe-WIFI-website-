from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
from wtforms import Form, StringField, SubmitField, validators, BooleanField, PasswordField, TimeField, SelectField
from wtforms.validators import DataRequired, Email, Length, URL, InputRequired
import csv
from datetime import datetime

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[InputRequired()])
    location_url = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField(label='Opening Time e.g. 8AM', validators=[InputRequired()])
    closing_time = StringField(label='Closing Time e.g. 5:30PM', validators=[InputRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField(label="Submit")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your key '
Bootstrap(app)


# class CafeForm(FlaskForm):
#      cafe = StringField('Cafe name', validators=[DataRequired()])
#      submit = SubmitField('Submit')


#e.g. You could use emojis ☕️/💪/✘/🔌


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == 'POST':
        cafe = form.cafe.data
        location_url = form.location_url.data
        open_time = form.open_time.data
        closing_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_rating = form.power_rating.data
        with open('cafe-data.csv', mode='a', encoding="utf-8") as csv_file:
            csv_file.write(f"\n{cafe},"
                         f"{form.location_url.data},"
                         f"{open_time},"
                         f"{closing_time},"
                         f"{coffee_rating},"
                         f"{wifi_rating},"
                         f"{power_rating}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
