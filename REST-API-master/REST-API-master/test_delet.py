from requests import delete, post

# корректный запрос
print(delete('http://localhost:5000/api/jobs/6').json())
# нет такого id
print(delete('http://localhost:5000/api/jobs/9999').json())
# некорректный запрос
print(delete('http://localhost:5000/api/jobs/ras').json())