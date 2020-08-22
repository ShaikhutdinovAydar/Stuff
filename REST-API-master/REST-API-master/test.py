from requests import get, post

print(get('http://localhost:5000/api/jobs').json())

print(get('http://localhost:5000/api/jobs/1').json())

print(get('http://localhost:5000/api/jobs/999').json())

print(get('http://localhost:5000/api/jobs/ras').json())

# Корректный запрос
print(post('http://localhost:5000/api/jobs',
           json={"id": 7,
                 'team_leader': 1,
                 'job': 'jobs decription',
                 'work_size': 21,
                 'collaborators': '1,2,3',
                 'is_finished': False,
                 'start_date': 'now',
                 'end_date': 'next week',
                 'creator_id': 1,
                 },
           ).json())

# Нет ключа job
print(post('http://localhost:5000/api/jobs',
           json={"id": 6,
                 'team_leader': 1,
                 'work_size': 21,
                 'collaborators': '1,2,3',
                 'is_finished': False,
                 'start_date': 'now',
                 'end_date': 'next week',
                 'creator_id': 1,
                 },
           ).json())
# Пустой запрос
print(post('http://localhost:5000/api/jobs',
           json={},
           ).json())
# получение работ
print(get('http://localhost:5000/api/jobs').json())
