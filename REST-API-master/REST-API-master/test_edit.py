from requests import get, post

# корректный запрос
print(post('http://localhost:5000/api/jobs/edit/4',
           json={
                 'team_leader': 1,
                 'work_size': 21,
                 'collaborators': '2,3',
                 'is_finished': True,
                 'start_date': '56',
                 'end_date': '43',
                 'creator_id': 1,
                 },
           ).json())
# нет такого collaborators, start_date, end_date, is_finished
print(post('http://localhost:5000/api/jobs/edit/4',
           json={
               'team_leader': 1,
               'work_size': 21,
               'collaborators': '1,2,3',
               'creator_id': 1,
           }, ).json())
# некорректный запрос
print(post('http://localhost:5000/api/jobs/edit/999',
           json={
               'team_leader': 1,
               'work_size': 21,
               'collaborators': '1,2,3',
               'creator_id': 1,
           }, ).json())
