# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

@app.route('/')
@app.route('/restaurants')
def showRestaurants() :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants) 

@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurant() :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    if request.method == 'POST' :
        newItem = Restaurant(name = request.form['name'])
        session.add(newItem)
        session.commit()
        flash("new restaurant created!")
        return redirect(url_for('showRestaurants'))
    return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id) :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    editedItem = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST' :
        if request.form['name'] :
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Restaurant name edited!")
        return redirect(url_for('showRestaurants'))
    return render_template('editRestaurant.html', restaurant = editedItem, restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id) :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    deleteItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST' :
        session.delete(deleteItem)
        session.commit()
        flash("Restaurant deleted!")
        return redirect(url_for('showRestaurants'))
    return render_template('deleterestaurant.html', restaurant = deleteItem)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
# korjaa tämä funktion nimenvaihdos tarpeellisiin paikkoihin
def showMenu(restaurant_id) :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items = items)   

# Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    if request.method == 'POST' :
        newItem = MenuItem(name = request.form['name'], description = request.form['description'], \
                           price = request.form['price'], course = request.form['course'], \
                           restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Create route for editMenuItem function here
# ADD ABILITY TO EDIT PRICE AND DESCRIPTION AND COURSE
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST' :
        if request.form['name'] :
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
            editedItem.price = request.form['price']
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("Menu item edited!")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)

# Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST' :
        session.delete(deleteItem)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = deleteItem)

# Making an API endpoint (GET request)
@app.route('/restaurants/JSON')
def restaurantsJSON() :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id) :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id) :
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(id= menu_id).one()
    return jsonify(MenuItem = item.serialize)

if __name__ == '__main__' :
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
