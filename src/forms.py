from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired
from sqlalchemy import inspect



class LoginFormFactory:
    @staticmethod
    def form():
        class F(FlaskForm):
            netid = StringField(default="Enter Your Netid")
        return F()

class AddStudentFormFactory:
    @staticmethod
    def form(restaurant, food, allergen):
        class F(FlaskForm):
            name = StringField(default="Enter Your Full Name")
            netid = StringField(default="Enter Your Netid")
            @staticmethod
            def restaurant_field_name(index):
                return 'restaurant_{}'.format(index)
            def restaurant_fields(self):
                for i, rest in enumerate(restaurant):
                    yield rest.name, getattr(self, F.restaurant_field_name(i))
            def get_restaurant_freq(self):
                for rest, field in self.restaurant_fields():
                    if field.data:
                        yield rest
						
            @staticmethod
            def food_field_name(index):
                return 'food_{}'.format(index)
            def food_fields(self):
                for i, foods in enumerate(food):
                    yield foods.name, getattr(self, F.food_field_name(i))
            def get_food_liked(self):
                for foods, field in self.food_fields():
                    if field.data != 0:
                        yield foods
						
						
            @staticmethod
            def allergen_field_name(index):
                return 'allergen_{}'.format(index)
            def allergen_fields(self):
                for i, allergens in enumerate(allergen):
                    yield allergens.allergenType, getattr(self, F.allergen_field_name(i))
            def get_allergens(self):
                for allergens, field in self.allergen_fields():
                    if field.data != 0:
                        yield allergens, field.data
        
	
							
        for i, rest in enumerate(restaurant):
            field_name = F.restaurant_field_name(i)
            setattr(F, field_name, BooleanField(default=0))
        	
        for i, foo in enumerate(food):
            field_name = F.food_field_name(i)
            setattr(F, field_name, BooleanField(default=0))

        for i, aller in enumerate(allergen):
            field_name = F.allergen_field_name(i)
            setattr(F, field_name, BooleanField(default=0))


        return F()


class StudentEditFormFactory:
    @staticmethod
    def form(student, restaurant, food, allergen):
        class F(FlaskForm):
            name = StringField(default=student.name)
            netid = StringField(default=student.netid)
            @staticmethod
            def restaurant_field_name(index):
                return 'restaurant_{}'.format(index)
            def restaurant_fields(self):
                for i, rest in enumerate(restaurant):
                    yield rest.name, getattr(self, F.restaurant_field_name(i))
            def get_restaurant_freq(self):
                for rest, field in self.restaurant_fields():
                    if field.data:
                        yield rest
						
            @staticmethod
            def food_field_name(index):
                return 'food_{}'.format(index)
            def food_fields(self):
                for i, foods in enumerate(food):
                    yield foods.name, getattr(self, F.food_field_name(i))
            def get_food_liked(self):
                for foods, field in self.food_fields():
                    if field.data != 0:
                        yield foods
						
						
            @staticmethod
            def allergen_field_name(index):
                return 'allergen_{}'.format(index)
            def allergen_fields(self):
                for i, allergens in enumerate(allergen):
                    yield allergens.allergenType, getattr(self, F.allergen_field_name(i))
            def get_allergens(self):
                for allergens, field in self.allergen_fields():
                    if field.data != 0:
                        yield allergens, field.data
								
        restaurant_freq = [restafreq.restaurant_name for restafreq in student.eats_at]
        for i, rest in enumerate(restaurant):
            field_name = F.restaurant_field_name(i)
            default = 'checked' if rest.name in restaurant_freq else None
            setattr(F, field_name, BooleanField(default=default))
        	
        food_liked = [foodlike.name for foodlike in student.eats]
        for i, foo in enumerate(food):
            field_name = F.food_field_name(i)
            default = 'checked' if foo.name in food_liked else None
            setattr(F, field_name, BooleanField(default=default))
        	
        allergic_to = [allerto.allergenType for allerto in student.is_allergic_to]
        for i, aller in enumerate(allergen):
            field_name = F.allergen_field_name(i)
            default = 'checked' if aller.allergenType in allergic_to else None
            setattr(F, field_name, BooleanField(default=default))


        return F()



class AttributeForm:
    attributes = SelectField(u'Attributes')

class SearchForm:
    @staticmethod
    def form(args):
        class G(FlaskForm):
            choices = [("Restaurant","Restaurant"),("Food","Food")]
            search = SelectField(u'Searching for a...', choices=choices)
            searches = FieldList(SelectField(u'Name'))
            labels = []


        g = G()

        for model in args:
                attributes = []
                mapper = inspect(model[1])
                for column in mapper.attrs:
                    attributes.append(column.key)
                select = SelectField(model[0],attributes)
                g.searches.append_entry()
                print attributes
                g.searches[len(g.searches)-1].choices=zip(attributes,attributes)
                g.labels.append(model[0])
                #searches.entries.append_entry(select)

        return g

        


