from flask import Flask, g, request, jsonify
from database import get_db, get_db_overview

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/overview', methods=['GET'])
def get_overview():
    db = get_db_overview()
    overview_cur = db.execute('SELECT id, "date", day_number,"day", breakfast_meal, breakfast_loc, lunch_meal, lunch_loc,'
                              'dinner_meal, dinner_loc, cal_total, carb_perc, protein_perc, fat_perc FROM overview')
    overview = overview_cur.fetchall()

    return_values = []
    for day in overview:
        day_dict = {}
        day_dict['id'] = day['id']
        day_dict['date'] = day['date']
        day_dict['day_number'] = day['day_number']
        day_dict['day'] = day['day']
        day_dict['breakfast_meal'] = day['breakfast_meal']
        day_dict['breakfast_loc'] = day['breakfast_loc']
        day_dict['lunch_meal'] = day['lunch_meal']
        day_dict['lunch_loc'] = day['lunch_loc']
        day_dict['dinner_meal'] = day['dinner_meal']
        day_dict['dinner_loc'] = day['dinner_loc']
        day_dict['cal_total'] = day['cal_total']
        day_dict['carb_perc'] = day['carb_perc']
        day_dict['protein_perc'] = day['protein_perc']
        day_dict['fat_perc'] = day['fat_perc']

        return_values.append(day_dict)

    return jsonify({"overview": return_values})

@app.route('/food', methods=['GET'])
def get_foods():
    db = get_db()
    foods_cur = db.execute('SELECT id, name, amount, measure, energy, carbs, sugar, protein, fat, description FROM foods')
    foods = foods_cur.fetchall()

    return_values = []

    for food in foods:
        food_dict = {}
        food_dict['id'] = food['id']
        food_dict['name'] = food['name']
        food_dict['amount'] = food['amount']
        food_dict['measure'] = food['measure']
        food_dict['energy'] = food['energy']
        food_dict['carbs'] = food['carbs']
        food_dict['sugar'] = food['sugar']
        food_dict['protein'] = food['protein']
        food_dict['fat'] = food['fat']
        food_dict['description'] = food['description']

        return_values.append(food_dict)

    return jsonify({'foods': return_values})

@app.route('/food/<int:food_id>', methods=['GET'])
def get_food(food_id):
    db = get_db()
    food_cur = db.execute('SELECT id, name, amount, measure, energy, carbs, sugar, protein, fat, description FROM foods WHERE id = ?', [food_id])
    food = food_cur.fetchone()

    return jsonify({'food': {'id': food['id'], 'name': food['name'], 'amount': food['amount'],
                             'measure': food['measure'], 'energy': food['energy'], 'carbs': food['carbs'],
                             'sugar': food['sugar'], 'protein': food['protein'], 'fat': food['fat'],
                             'description': food['description']}})

@app.route('/food', methods=['POST'])
def add_food():
    new_food_data = request.get_json()

    name = new_food_data["name"]
    amount = new_food_data["amount"]
    measure = new_food_data["measure"]
    energy = new_food_data["energy"]
    carbs = new_food_data["carbs"]
    sugar = new_food_data["sugar"]
    protein = new_food_data["protein"]
    fat = new_food_data["fat"]
    descr = new_food_data["description"]

    db = get_db()
    db.execute('INSERT INTO foods (name, amount, measure, energy, carbs, sugar, protein, fat, description) VALUES (?,?,?,?,?,?,?,?,?)',
               [name, amount, measure, energy, carbs, sugar, protein, fat, descr])
    db.commit()

    food_cur = db.execute('SELECT id, name, amount, measure, energy, carbs, sugar, protein, fat, description FROM foods WHERE name = ?', [name])
    new_food = food_cur.fetchone()

    return jsonify({'food': {'id': new_food['id'], 'name': new_food['name'], 'amount': new_food['amount'],
                             'measure': new_food['measure'], 'energy': new_food['energy'], 'carbs': new_food['carbs'],
                             'sugar': new_food['sugar'], 'protein': new_food['protein'], 'fat': new_food['fat'],
                             'description': new_food['description']}})

@app.route('/overview', methods=['POST'])
def add_day():
    new_day_data = request.get_json()

    date = new_day_data['date']
    day_number = new_day_data['day_number']
    day = new_day_data['day']
    breakfast_meal = new_day_data['breakfast_meal']
    breakfast_loc = new_day_data['breakfast_loc']
    lunch_meal = new_day_data['lunch_meal']
    lunch_loc = new_day_data['lunch_loc']
    dinner_meal = new_day_data['dinner_meal']
    dinner_loc = new_day_data['dinner_loc']
    cal_total = new_day_data['cal_total']
    carb_perc = new_day_data['carb_perc']
    protein_perc = new_day_data['protein_perc']
    fat_perc = new_day_data['fat_perc']

    db = get_db_overview()
    db.execute('INSERT INTO overview (date, day_number, day, breakfast_meal, breakfast_loc, lunch_meal, lunch_loc,'
               'dinner_meal, dinner_loc, cal_total, carb_perc, protein_perc, fat_perc) VALUES (?, ?, ?, ?, ?, ?, ?, ?,'
               ' ?, ?, ?, ?, ?)', [date, day_number, day, breakfast_meal, breakfast_loc, lunch_meal, lunch_loc,
                                   dinner_meal, dinner_loc, cal_total, carb_perc, protein_perc, fat_perc])
    db.commit()

    overview_cur = db.execute('SELECT id, "date", day_number, "day", breakfast_meal, breakfast_loc, lunch_meal, lunch_loc,'
               'dinner_meal, dinner_loc, cal_total, carb_perc, protein_perc, fat_perc FROM OVERVIEW WHERE date = ?', [date])

    new_day = overview_cur.fetchone()

    return jsonify({'day': {'id': new_day['id'], 'date': new_day['date'], 'day_number': new_day['date'],
                            'day': new_day['day'], 'breakfast_meal': new_day['breakfast_meal'],
                            'breakfast_loc': new_day['breakfast_loc'], 'lunch_meal': new_day['lunch_meal'],
                            'lunch_loc': new_day['lunch_loc'], 'dinner_meal': new_day['dinner_meal'],
                            'dinner_loc': new_day['dinner_loc'], 'cal_total': new_day['cal_total'],
                            'carb_perc': new_day['carb_perc'], 'protein_perc': new_day['protein_perc'],
                            'fat_perc': new_day['fat_perc']}})


@app.route('/food/<int:food_id>', methods=['PUT', 'PATCH'])
def edit_food(food_id):
    edit_food_data = request.get_json()

    name = edit_food_data["name"]
    amount = edit_food_data["amount"]
    measure = edit_food_data["measure"]
    energy = edit_food_data["energy"]
    carbs = edit_food_data["carbs"]
    sugar = edit_food_data["sugar"]
    protein = edit_food_data["protein"]
    fat = edit_food_data["fat"]
    descr = edit_food_data["description"]

    db = get_db()
    db.execute('UPDATE foods SET name = ?, amount = ?, measure = ?, energy = ?, carbs = ?, sugar = ?, protein = ?, fat = ?,'
               ' description = ? WHERE id = ?', [name, amount, measure, energy, carbs, sugar, protein, fat, descr, food_id])
    db.commit()

    food_cur = db.execute('SELECT id, name, amount, measure, energy, carbs, sugar, protein, fat, description FROM foods WHERE id = ?', [food_id])
    edited_food = food_cur.fetchone()

    return jsonify({'food': {'id': edited_food['id'], 'name': edited_food['name'], 'amount': edited_food['amount'],
                             'measure': edited_food['measure'], 'energy': edited_food['energy'],
                             'carbs': edited_food['carbs'], 'sugar': edited_food['sugar'],
                             'protein': edited_food['protein'], 'fat': edited_food['fat'],
                             'description': edited_food['description']}})

@app.route('/food/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    db = get_db()
    db.execute('DELETE from foods WHERE id = ?', [food_id])
    db.commit()

    return jsonify({'message': 'The food has been deleted!'})

if __name__ == '__main__':
    app.run(debug=True)
