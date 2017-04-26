from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import datetime

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
loginstatus = False
user = None

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = forms.LoginFormFactory.form()
    if form.validate_on_submit():
        if request.form.get('login', None) == "Login":
            user = db.session.query(models.Student).filter(models.Student.netid == form.netid.data).one()
            if user is not None:
                loginstatus = True
                return redirect(url_for('welcome', netid = user.netid, openRestaurants=[]))
            else:
                error = 'Invalid NetID.'	
            return render_template('login.html', form=form, error=error)
        else:
            return redirect(url_for('add_student'))   
    return render_template('login.html', form=form, error=error)


@app.route("/logout")
def logout():
    loginstatus = False
    flash('You were logged out.')
    return redirect(home())

@app.route('/all-restaurants')
def all_restaurants():
    restaurants = db.session.query(models.Restaurant).all()
    return render_template('all-restaurants.html', restaurants=restaurants)

@app.route('/all-foods')
def all_foods():
    foods = db.session.query(models.Food).all()
    return render_template('all-foods.html', foods=foods)

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
    allergies = db.session.query(models.IsAllergicTo)\
        .filter(models.IsAllergicTo.student_netid == netid)
    favoriteRestaurants = db.session.query(models.EatsAt)\
        .filter(models.EatsAt.student_netid == netid)
    favoriteFoods = db.session.query(models.Eats)\
        .filter(models.Eats.student_netid == netid)
    medications = []
    for aller in allergies:
        allergen = db.session.query(models.Allergens)\
            .filter(models.Allergens.allergenType ==aller.allergenType).first()
        if(allergen is not None):
            medications.append(allergen.medication)
		
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
    return render_template('welcome.html', netid=netid,openRestaurants=openRestaurants, favoriteFoods=favoriteFoods, medication=medications)

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
            user = netid=form.netid.data
            db.session.commit()
            return redirect(url_for('welcome', netid=form.netid.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('add-Student.html', form=form)
    else:
        return render_template('add-Student.html', form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    l = []
    

    l.append(("Restaurant",models.Restaurant))
    l.append(("Food",models.Food))
    form = forms.SearchForm.form(l)
    #l.append(("Serves",models.Serves))
    
    if form.is_submitted():
        try:
            textSearchTables = [("Food","name"),("Restaurant","location"),("Restaurant","name")]
            numberSearchTables = [("Food","calories")]
            queryList = []
            counter = 0
            while form.textSearches.__len__() > 0:
                entry = form.textSearches.pop_entry()
                print entry.select.data

                #print entry.label
                #print entry.select.choices
                if(entry.myLabel == ""):
                    print entry.myLabel
                    table = textSearchTables[counter][0]
                    column = textSearchTables[counter][1]
                    filterType = entry.select.data
                    criteria = entry.criteria.data
                    queryList.append((table,column, str(filterType), str(criteria)))
                    counter+=1
            counter = 0
            while form.numberSearches.__len__() > 0:
                entry = form.numberSearches.pop_entry()
                print entry.select.data
                #print entry.label
                #print entry.select.choices
                if(entry.myLabel == ""):
                    print entry.myLabel
                    table = numberSearchTables[counter][0]
                    column = numberSearchTables[counter][1]
                    filterType = entry.select.data
                    criteria = entry.criteria.data
                    queryList.append((table,column, str(filterType), str(criteria)))
                    counter+=1
                
            bigTable = db.session.query(models.Restaurant,models.Food,models.Serves).filter(models.Restaurant.name == models.Serves.restaurant_name).\
            filter(models.Serves.food_name == models.Food.name).add_columns(models.Restaurant.name,models.Restaurant.location,models.Serves.food_name,models.Food.calories).all()
            filteredResult = []
            textDict = {
            'like': (lambda str1, str2: str2.upper() in str1.upper()),
            'starts': (lambda str1, str2: str1.upper().startswith(str2.upper())),
            'ends':(lambda str1, str2: str1.upper().endswith(str2.upper())),
            'equals':(lambda str1, str2: str1.upper()==str2.upper())
            }

            for result in bigTable:
                add = True
                for query in queryList:
                    print query
                    if(query[3]=="" or query[3] is None or query[3]=='None'):
                        continue
                    if(query[0]=="Restaurant"):
                        if(query[1]=="name"):
                            if(not textDict[query[2]](result.name,query[3])):
                                add = False
                        if(query[1]=="location"):
                            if(not textDict[query[2]](result.location,query[3])):
                                add = False
                    if(query[0]=="Food"):
                        if(query[1]=="name"):
                            print(result.food_name, " food name")
                            print textDict[query[2]](result.food_name,query[3])
                            if(not textDict[query[2]](result.food_name,query[3])):
                                add = False
                        if(query[1]=="calories"):
                            if(query[2]==">"):
                                add = int(query[3]) <= int(result.calories)
                            if(query[2]=="<"):
                                add = int(query[3]) >= int(result.calories)


                if(add):
                    filteredResult.append(result)
                justRestaurants = []
                for r in filteredResult:
                    justRestaurants.append(r.name)
                print result.name
            #print(bigTable)
            #rest_serves = rest.query.join(serves,rest.name==serves.restaurant_name).add_columns(rest.name, rest.location, serves.food_name,serves.price)
            #bigTable = rest_serves.query.join(food,rest_serves.food_name==food.name)
            #print bigTable
            
            return render_template('results.html', results=filteredResult, column=form.search.data, restaurants=set(justRestaurants))
        except BaseException as e:
            form.errors['database'] = str(e)
            print e
            print "error here"
            return render_template('search.html',form=form)
    
    
    else:
    #    print("error NOW")
        return render_template('search.html',form=form)

@app.route('/edit-student/<netid>', methods=['GET', 'POST'])
def edit_student(netid):
    student = db.session.query(models.Student)\
        .filter(models.Student.netid == netid).one()
    restaurant = db.session.query(models.Restaurant).all()
    food = db.session.query(models.Food).all()
    allergen = db.session.query(models.Allergens).all()
    form = forms.StudentEditFormFactory.form(student, restaurant, food, allergen)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Student.edit(form.name.data, student.netid, form.netid.data,
                                form.get_restaurant_freq(), form.get_food_liked(),
							   form.get_allergens())
            return redirect(url_for('welcome', netid=form.netid.data))
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
