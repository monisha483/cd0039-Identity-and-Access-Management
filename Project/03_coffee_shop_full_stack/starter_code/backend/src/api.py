import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drink_selection = Drink.query.order_by(Drink.id).all()
    if(len(drink_selection)==0):
        abort(404)
    return jsonify({"success": True, "drinks": [drink.short() for drink in drink_selection]})
    


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(self):
    drink_selection = Drink.query.order_by(Drink.id).all()
    if(len(drink_selection)==0):
        abort(404)
    # drinkDict = {}
    # for drink in drink_selection:
    #     drinkDict[drink.id] = drink.long()
    return jsonify({"success": True, "drinks": [drink.long() for drink in drink_selection]})
    

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def insert_drink(self):
    print('hi')
    body = request.get_json()
    print('body')
    new_recipe = body.get('recipe', None)
    print('recipe ', new_recipe)
    new_title = body.get('title', None)
    print('title ', new_title)
    #new_category = body.get('category', None)
    #new_difficulty = body.get('difficulty', None)
    try:
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        print('drink ', drink)
        drink.insert()
        print('inserted!', drink.long())
        return jsonify({"success": True, "drinks": drink.long()})
    except Exception:
        abort(422)

    
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(self, id):
    print("update_drink!!")
    drink = Drink.query.get(id)
    print("patch drink!!", drink)
    if(drink is None):
        abort(401)
    body = request.get_json()
    print('body')
    new_recipe = body.get('recipe', None)
    print('recipe ', new_recipe)
    new_title = body.get('title', None)
    try:
        drink.title = new_title
        drink.recipe = json.dumps(new_recipe)
        print('drink ', drink)
        drink.update()
        print('inserted!', drink.long())
        return jsonify({"success": True, "drinks": [drink.long()]})
    except Exception:
        abort(422)
    

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(self, id):
    drink = Drink.query.get(id)
    if(drink is None):
        abort(401)
    try:
        drink.delete()
        print('deleted!')
        return jsonify({"success": True, "delete": id})
    except Exception:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "notfound"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def unauthorised(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorised"
    }), 401


@app.errorhandler(500)
def internalservererror(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403