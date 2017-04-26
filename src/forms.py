from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired
from sqlalchemy import inspect
from collections import namedtuple


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


class NumberForm(FlaskForm):
    myLabel = ""
    choices = [(">","greater than"),("<","less than")]
    select = SelectField(u'filter',choices=choices)
    criteria = IntegerField()
class TextForm(FlaskForm):
    myLabel = ""

    choices = [("like","contains"),("starts","starts with"),("ends","ends with"),("equals","is exactly")]
    select = SelectField(u'filter',choices=choices,default='')
    criteria = StringField(default="")
        
    def init(self,label):
        myLabel = label
    # @staticmethod
    # def form(label):
    #     class F(FlaskForm):
    #         critera = StringField(default="Search...")
    #         myLabel = ""
    #         choices = [("like","contains"),("starts","starts with"),("ends","ends with"),("equals","is exactly")]
    #         select = SelectField(u'filter',choices=choices)
    #         def init(self,label):
    #             myLabel = label
    #     f = F()
    #     f.init(label)
    #     return f

class MiniSearchForm(FlaskForm):
    myHeader = ""
    textSearches = FieldList(FormField(TextForm))
    numberSearches = FieldList(FormField(NumberForm))

    

class SearchForm:
    @staticmethod
    def form(args):
        class G(FlaskForm):
            choices = [("Restaurant","Restaurant"),("Food","Food")]
            search = SelectField(u'Searching for a...', choices=choices)
            #searches = FieldList(SelectField(u'Name'))
            textSearches = FieldList(FormField(TextForm))
            numberSearches = FieldList(FormField(NumberForm))
            searches = FieldList(FormField(MiniSearchForm))
            sections = {}

            labels = []


        g = G()

        for model in args:
                attributes = []
                mapper = inspect(model[1])
                print mapper
                for column in mapper.columns:
                    print str(column.type)[0:7]
                    print column.key
                    if(str(column.type)[0:7] == "VARCHAR"):
                        f = TextForm()
                        f.init(column.key)
                        Tf = namedtuple('TextForm',['myLabel'])
                        t1 = Tf(column.key)
                        g.textSearches.append_entry()
                        g.textSearches[len(g.textSearches)-1].myLabel = model[0] + " " + column.key
                        g.labels.append(model[0]+ " " +column.key)
                        #g.textSearches[len(g.textSearches)-1] = f
                    if(str(column.type)== "INTEGER"):
                        g.numberSearches.append_entry()
                        g.numberSearches[len(g.numberSearches)-1].myLabel = model[0] + " " + column.key
                        g.labels.append(model[0]+ " " +column.key)
                    attributes.append(column.key)
                # select = SelectField(model[0],attributes)
                # g.searches.append_entry()
                # print attributes
                # g.searches[len(g.searches)-1].choices=zip(attributes,attributes)
                # g.labels.append(model[0])
                #searches.entries.append_entry(select)
        print "making search form"
        print len(g.textSearches.entries)
        return g

        


