from requests import get, post, delete

print(get('http://localhost:5000/api/users').json())

print(get('http://localhost:5000/api/user/1').json())

print(get('http://localhost:5000/api/user/1000').json())

print(get('http://localhost:5000/api/user/ras').json())

print(post('http://localhost:5000/api/user',
           json={"id": 4,
                 'name': "Andrey",
                 'surname': 'Petrov',
                 'age': 21,
                 'position': 'gh',
                 'speciality': "fg",
                 'address': 'Almet',
                 'email': 'Petrov@mail.ru',
                 'hashed_password': 'test',
                 },
           ).json())

print(post('http://localhost:5000/api/user',
           json={
               'name': "Andrey",
               'speciality': "fg",
               'address': 'Almet',
               'email': 'Petrov@mail.ru',
               'hashed_password': 'test',
           },
           ).json())

print(post('http://localhost:5000/api/user/edit/3',
           json={
               'name': "Andrey",
               'speciality': "fg",
               'address': 'Almet',
               'hashed_password': 'test',
           },
           ).json())

# корректный запрос
print(delete('http://localhost:5000/api/users/4').json())
# нет такого id
print(delete('http://localhost:5000/api/users/9999').json())
# некорректный запрос
print(delete('http://localhost:5000/api/users/ras').json())
