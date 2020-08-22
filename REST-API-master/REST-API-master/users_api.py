import flask
import requests
from data import db_session
from data.jobs import Jobs
from flask import jsonify, request, render_template
import datetime
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    connect = db_session.create_session()
    users = connect.query(User).all()
    return jsonify(
        {
            'Users':
                [item.to_dict()
                 for item in users]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    connect = db_session.create_session()
    user = connect.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'User': user.to_dict()
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request - tt'})
    connect = db_session.create_session()
    exist = connect.query(User).filter(User.id == request.json['id']).first()
    if exist:
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        modified_date=datetime.datetime.now()
    )
    user.set_password(request.json['hashed_password'])
    connect.add(user)
    connect.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:job_id>', methods=['DELETE'])
def delete_user(user_id):
    connect = db_session.create_session()
    user = connect.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found - no user'})
    connect.delete(user)
    connect.commit()
    return jsonify({'success': 'OK - user deleted'})


@blueprint.route('/api/user/edit/<int:user_id>', methods=['POST'])
def edit_user_json(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    connect = db_session.create_session()
    user = connect.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'not Found - job was not found'})
    if not any([key in request.json for key in
                ['id', 'surname', 'name', 'age', 'position',
                 'speciality', 'address', 'email', 'hashed_password']]):
        return jsonify({'error': 'Bad request - user'})
    for key in request.json:
        if key == 'id':
            user.id = request.json['id']
        if key == 'surname':
            user.surname = request.json['surname']
        if key == 'name':
            user.name = request.json['name']
        if key == 'age':
            user.age = request.json['age']
        if key == 'position':
            user.position = request.json['position']
        if key == 'speciality':
            user.speciality = request.json['speciality']
        if key == 'address':
            user.address = request.json['address']
        if key == 'email':
            user.email = request.json['email']
        if key == 'hashed_password':
            user.set_password(request.json['hashed_password'])
    connect.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/users_show/<int:user_id>', methods=['GET'])
def user_show(user_id):
    connect = db_session.create_session()
    user = connect.query(User).filter(User.id == user_id).first()

    response = requests.get(f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={user.city_from}&format=json")
    if not response:
        return jsonify({"error": "Упс..."})
    else:
        json_response = response.json()
        json_response = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if len(json_response) == 0:
            return jsonify({"error": "error"})
        toponym = json_response[0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        coords = toponym_coodrinates.split()

    params = {
        'spn': '0.05,0.05',
        "ll": ",".join(coords),
        "l": 'sat',
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    }
    geocoder_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_server, params=params)
    with open(f"static/img/{user.city_from}.png", "wb") as file:
        file.write(response.content)
    return render_template('show.html', name=user.name,surname=user.surname,src=f'/static/img/{user.city_from}.png', hometown=user.city_from)