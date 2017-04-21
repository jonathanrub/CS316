from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import datetime

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

@app.route('/')
def all_restaurants():
    restaurants = db.session.query(models.Restaurant).all()
    return render_template('all-restaurants.html', restaurants=restaurants)

@app.route('/restaurant/<name>')
def restaurant(name):
    restaurant = db.session.query(models.Restaurant)\
        .filter(models.Restaurant.name == name).one()
    return render_template('restaurant.html', restaurant=restaurant)

@app.route('/food/<name>')
def food(name):
    food = db.session.query(models.Food)\
        .filter(models.Food.name == name).one()
    return render_template('food.html',food=food)
# @app.route('/edit-restaurant/<name>', methods=['GET', 'POST'])
# def edit_restaurant(name):
#     restaurant = db.session.query(models.Restaurant)\
#         .filter(models.restaurant.name == name).one()
#     beers = db.session.query(models.Beer).all()
#     bars = db.session.query(models.Bar).all()
#     form = forms.restaurantEditFormFactory.form(restaurant, beers, bars)
#     if form.validate_on_submit():
#         try:
#             form.errors.pop('database', None)
#             models.Restaurant.edit(name, form.name.data, form.address.data,
#                                 form.get_beers_liked(), form.get_bars_frequented())
#             return redirect(url_for('restaurant', name=form.name.data))
#         except BaseException as e:
#             form.errors['database'] = str(e)
#             return render_template('edit-restaurant.html', restaurant=restaurant, form=form)
#     else:
#         return render_template('edit-restaurant.html', restaurant=restaurant, form=form)

@app.route('/welcome/<netid>')
def welcome(netid):
    student = db.session.query(models.Student)\
        .filter(models.Student.netid == netid).one()
    favoriteRestaurants = db.session.query(models.EatsAt)\
        .filter(models.EatsAt.student_netid == student.netid)
    openRestaurants = []
    for rest in favoriteRestaurants:
        day = datetime.datetime.now().weekday()+1
        isopen = db.session.query(models.IsOpen)\
            .filter(models.IsOpen.day_of_the_week == day, models.IsOpen.restaurant_name==rest.restaurant_name).first()
        time = (datetime.datetime.now()-datetime.timedelta(hours=4)).hour + float(datetime.datetime.now().minute)/60  
        if(isopen is None):
            continue 
        if(isopen.open_time <= time and isopen.close_time >= time):
            openRestaurants.append(rest)
    return render_template('welcome.html',student=student,openRestaurants=openRestaurants)

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    restaurant = db.session.query(models.Restaurant).all()
    food = db.session.query(models.Food).all()
    allergen = db.session.query(models.Allergens).all()
    form = forms.AddStudentFormFactory.form(restaurant, food, allergen)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Student.add(form.name.data, form.netid.data,
                                form.get_restaurant_freq(), form.get_food_liked(),
							   form.get_allergens())
            return redirect('welcome/' + form.netid.data
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('add-Student.html', form=form)
    else:
        return render_template('add-Student.html', form=form)

@app.route('/edit-student/<name>', methods=['GET', 'POST'])
def edit_student(name):
    student = db.session.query(models.Student)\
        .filter(models.Student.name == name).one()
    restaurant = db.session.query(models.Restaurant).all()
    food = db.session.query(models.Food).all()
    allergen = db.session.query(models.Allergens).all()
    form = forms.StudentEditFormFactory.form(student, restaurant, food, allergen)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Student.edit(name, form.name.data, student.netid, form.netid.data,
                                form.get_restaurant_freq(), form.get_food_liked(),
							   form.get_allergens())
            return redirect(url_for('edit_student', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-student.html', student=student, form=form)
    else:
        return render_template('edit-student.html', student=student, form=form)


@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
