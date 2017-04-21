from sqlalchemy import sql, orm
from app import db

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    name = db.Column('name', db.String(30), primary_key=True)
    location = db.Column('location', db.String(20))
    is_food_truck = db.Column('is_food_truck',db.Boolean())
    is_open = orm.relationship('IsOpen')
    serves = orm.relationship('Serves')
    # @staticmethod
    # def edit(old_name, name, address, beers_liked, bars_frequented):
    #     try:
    #         db.session.execute('DELETE FROM likes WHERE drinker = :name',
    #                            dict(name=old_name))
    #         db.session.execute('DELETE FROM frequents WHERE drinker = :name',
    #                            dict(name=old_name))
    #         db.session.execute('UPDATE drinker SET name = :name, address = :address'
    #                            ' WHERE name = :old_name',
    #                            dict(old_name=old_name, name=name, address=address))
    #         for beer in beers_liked:
    #             db.session.execute('INSERT INTO likes VALUES(:drinker, :beer)',
    #                                dict(drinker=name, beer=beer))
    #         for bar, times_a_week in bars_frequented:
    #             db.session.execute('INSERT INTO frequents'
    #                                ' VALUES(:drinker, :bar, :times_a_week)',
    #                                dict(drinker=name, bar=bar,
    #                                     times_a_week=times_a_week))
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         raise e
class IsOpen(db.Model):
    __tablename__ = 'isopen'
    restaurant_name = db.Column('restaurant_name',db.String(30), db.ForeignKey('restaurant.name'), primary_key=True)
    day_of_the_week = db.Column('day_of_the_week',db.Integer(), primary_key = True)
    open_time = db.Column('open_time',db.Float())
    close_time = db.Column('close_time',db.Float())

class Merchant(db.Model):
    __tablename__ = 'merchant'
    restaurant_name = db.Column('restaurant_name',db.String(30), db.ForeignKey('restaurant.name'), primary_key=True)
    phonenumber = db.Column('phonenumber',db.Integer())

class Food(db.Model):
    __tablename__ = 'food'
    name = db.Column('name',db.String(40),primary_key=True)
    calories = db.Column('calories',db.Integer())
    allergens = orm.relationship('HasAllergen')

class Serves(db.Model):
    __tablename__ = 'serves'
    restaurant_name = db.Column('restaurant_name',db.String(30),db.ForeignKey('restaurant.name'), primary_key=True)
    food_name = db.Column('food_name',db.String(40),db.ForeignKey('food.name'), primary_key = True)
    price = db.Column('price',db.Float())

class Student(db.Model):
    __tablename__ = 'student'
    netid = db.Column('netid',db.String(10),primary_key=True)
    name = db.Column('name',db.String(40))
    foodplan = db.Column('foodpoint_plan',db.String(1))
    eats_at = orm.relationship('EatsAt')
    eats = orm.relationship('Eats')
    is_allergic_to = orm.relationship('IsAllergicTo')
    @staticmethod
    def edit(old_name, name, old_netid, netid, restaurant_freq, food_liked, allergic_to):
        try:
            db.session.execute('DELETE FROM eatsat WHERE student_netid = :netid',dict(netid=old_netid))
            db.session.execute('DELETE FROM eats WHERE student_netid = :netid',dict(netid=old_netid))
            db.session.execute('DELETE FROM isallergicto WHERE student_netid = :netid',dict(netid=old_netid))
            db.session.execute('UPDATE student SET name = :name, netid = :netid WHERE netid = :old_netid',dict(old_name=old_name, name=name, old_netid=old_netid, netid=netid))
			
            for rest in restaurant_freq:
                db.session.execute('INSERT INTO eatsat VALUES(:student_netid, :restaurant_name)',dict(student_netid=netid, restaurant_name=rest))

            for foo in food_liked:
                db.session.execute('INSERT INTO eats VALUES(:student_netid, :food_name)',dict(student_netid=netid, food_name=foo))
            for aller in allergic_to:
                db.session.execute('INSERT INTO isallergicto VALUES(:allergenType, :student_netid)',dict(student_netid=netid, allergenType=aller[0]))         
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class EatsAt(db.Model):
    __tablename__ = 'eatsat'
    student_netid = db.Column('student_netid',db.String(10),db.ForeignKey('student.netid'),primary_key = True)
    restaurant_name = db.Column('restaurant_name',db.String(30),db.ForeignKey('restaurant.name'), primary_key=True)

class Eats(db.Model):
    __tablename__ = 'eats'
    student_netid = db.Column('student_netid',db.String(10),db.ForeignKey('student.netid'),primary_key = True)
    food_name = db.Column('food_name',db.String(40),db.ForeignKey('food.name'),primary_key=True)

class Allergens(db.Model):
    __tablename__ = 'allergens'
    allergenType = db.Column('type',db.String(50),primary_key=True)
    medication = db.Column('medication',db.String(50))

class HasAllergen(db.Model):
    __tablename__ = 'hasallergen'
    allergenType = db.Column('allergen_type',db.String(50),db.ForeignKey('allergens.type'),primary_key=True)
    food_name = db.Column('food_name',db.String(40),db.ForeignKey('food.name'),primary_key=True)

class IsAllergicTo(db.Model):
    __tablename__ = 'isallergicto'
    allergenType = db.Column('allergen_type',db.String(50),db.ForeignKey('allergens.type'),primary_key=True)
    student_netid = db.Column('student_netid',db.String(10),db.ForeignKey('student.netid'),primary_key = True)

