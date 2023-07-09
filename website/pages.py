from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from .helpers import get_nutrition_info
from .database import db, Food
from datetime import datetime, date

pages = Blueprint('pages', __name__)

@pages.route("/", methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('pages.diary'))
    else:
        return redirect(url_for('auth.login'))

@pages.route("/diary", methods=['GET','POST'])
@login_required
def diary():
    return render_template("diary.html")

@pages.route("/foods", methods=['GET','POST'])
@login_required
def foods():
    if request.method == 'POST':
        food_name = request.form.get("food")
        food_quantity = request.form.get("quantity")
        food =  food_quantity + " " + food_name
        if not food_name or not food_quantity:
            flash('Invalid Query', category='error')
        if int(food_quantity) <= 0:
            flash('Must enter a positive quantity', category='error')
        nutrition_info = get_nutrition_info(food)
    else:
        nutrition_info = None
    
    return render_template("foods.html", nutrition_info=nutrition_info)



@pages.route("/targets", methods=['GET','POST'])
@login_required
def targets():
    if request.method == 'GET':
        return render_template("targets.html")
    
    calories = request.form.get('calories')
    protein = request.form.get('protein')
    carbohydrates = request.form.get('carbohydrates')
    fats = request.form.get('fat')

    if not all((calories, protein, carbohydrates, fats)):
        flash('Invalid target values', category='error')
    elif not all(value.isdigit() and int(value) >= 0 for value in (calories, protein, carbohydrates, fats)):
        flash('Invalid target values', category='error')
    else:
        current_user.calories = float(calories)
        current_user.protein = float(protein)
        current_user.carbohydrates = float(carbohydrates)
        current_user.fats = float(fats)
        db.session.commit()
        flash('Targets updated successfully!', category='success')
        return redirect(url_for('pages.targets'))
    
    return render_template("targets.html")

@pages.route("/addToDiary", methods=['POST'])
@login_required
def addToDiary():
    if request.method == 'POST':
        name = request.form.get('name')
        carbs = request.form.get('carbs')
        fat = request.form.get('fat')
        protein = request.form.get('protein')
        calories = request.form.get('calories')
        user_id = current_user.id
        new_food = Food(name=name, carbs=carbs, fat=fat, protein=protein, calories=calories, user_id=user_id)
        db.session.add(new_food)
        db.session.commit()
        flash('Food added to Diary', category='success')
        return redirect(url_for('pages.diary'))
    
    return render_template("foods.html")


@pages.route("/foodLog", methods=['POST'])
@login_required
def foodLog():
    if request.method == 'POST':
        date_str = request.form.get('date')
        if not date_str:
            flash('Select a date', category='error')
            return redirect(url_for('pages.diary'))
        

        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        foods = Food.query.filter_by(user_id=current_user.id, date=selected_date).all()
        formatted_date = selected_date.strftime('%B %d, %Y')
        
        total_calories = round(sum(food.calories for food in foods), 2)
        total_fat = round(sum(food.fat for food in foods), 2)
        total_protein = round(sum(food.protein for food in foods), 2)
        total_carbs = round(sum(food.carbs for food in foods), 2)
        
        return render_template("diary.html", foods=foods, formatted_date=formatted_date, total_calories=total_calories, total_protein=total_protein, total_carbs=total_carbs, total_fat=total_fat)

    return redirect(url_for('pages.food'))

@pages.route("/removeFromFoodLog/<int:food_id>", methods=['POST'])
@login_required
def removeFromFoodLog(food_id):
    food = Food.query.get(food_id)
    if food:
        db.session.delete(food)
        db.session.commit()
        flash('Food entry removed successfully!', category='success')
    else:
        flash('Food entry not found', category='error')

    return redirect(url_for('pages.diary'))

