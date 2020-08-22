import flask
from data import db_session
from data.jobs import Jobs
from flask import jsonify, request

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    connect = db_session.create_session()
    jobs = connect.query(Jobs).all()
    return jsonify(
        {
            'Jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_news(job_id):
    connect = db_session.create_session()
    job = connect.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'Job': job.to_dict()
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished', 'creator_id']):
        return jsonify({'error': 'Bad request'})
    connect = db_session.create_session()
    exist = connect.query(Jobs).filter(Jobs.id == request.json['id']).first()
    if exist:
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished'],
        creater_id=request.json['creator_id']
    )
    connect.add(job)
    connect.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/edit/<int:job_id>', methods=['POST'])
def edit_job_json(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    connect = db_session.create_session()
    job = connect.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'not Found - job was not found'})
    if not any([key in request.json for key in
                ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                 'start_date', 'end_date', 'is_finished', 'creator_id']]):
        return jsonify({'error': 'Bad request'})
    for key in request.json:
        if key == 'id':
            job.id = request.json['id']
        if key == 'team_leader':
            job.team_leader = request.json['team_leader']
        if key == 'job':
            job.job = request.json['job']
        if key == 'work_size':
            job.work_size = request.json['work_size']
        if key == 'collaborators':
            job.collaborators = request.json['collaborators']
        if key == 'start_date':
            job.start_date = request.json['start_date']
        if key == 'end_date':
            job.end_date = request.json['end_date']
        if key == 'is_finished':
            job.is_finished = request.json['is_finished']
        if key == 'creator_id':
            job.creater_id = request.json['creator_id']
    connect.commit()
    return jsonify({'success': 'OK'})
