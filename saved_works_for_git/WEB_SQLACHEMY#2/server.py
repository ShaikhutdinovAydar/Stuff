from flask import Flask
import datetime
from data import db_session

from WEB_SQLACHEMY.data.users import User
from WEB_SQLACHEMY.data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/ mars_explorer.db")
    user = Jobs()
    user.team_leader = 1
    user.job = "deployment of residential modules 1 and 2"
    user.work_size = 15
    user.position = "captain"
    user.collaborators = '2, 3'
    user.address = "module_1"
    user.start_date = datetime.datetime.now()
    user.is_finished = False
    session = db_session.create_session()
    session.add(user)
    session.commit()
    app.run()


if __name__ == '__main__':
    main()
