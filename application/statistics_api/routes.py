# application/statistics_api/routes.py

from . import statistics_api_blueprint
from .. import db
from ..models import Stat
from datetime import datetime
from flask import make_response, request, jsonify


@statistics_api_blueprint.route('/api/stats', methods=['GET'])
def get_stats():
    data = []
    for row in Stat.query.all():
        data.append(row.to_json())

    response = jsonify(data)
    return response


@statistics_api_blueprint.route('/api/stat/create', methods=['POST'])
def post_create():
    project_id = request.json['project_id']
    user_id = request.json['user_id']
    ticket_id = request.json['ticket_id']
    ticket_status = request.json['ticket_status']
    project_status = request.json['project_status']

    stat = Stat()
    stat.project_id = project_id
    stat.user_id = user_id
    stat.ticket_id = ticket_id
    stat.ticket_status = ticket_status
    stat.project_status = project_status

    db.session.add(stat)
    db.session.commit()

    response = jsonify({'message': 'Stat added', 'result': stat.to_json()})
    return response


@statistics_api_blueprint.route('/api/stat/average-time', methods=['GET'])
def get_average_time():
    res = Stat.query.filter(Stat.date_finished!=None).all()
    time = 0
    for row in res:
        date_format_str = '%Y-%m-%d %H:%M:%S.%f'
        start = datetime.strptime(str(row.to_json()['date_created']), date_format_str)
        end = datetime.strptime(str(row.to_json()['date_finished']), date_format_str)
        diff = end - start
        diff_in_minutes = diff.total_seconds() / 60
        time += diff.total_seconds() / 60
    result = "there is not finished task to calculate average time" if not res else time/len(res)
    return jsonify({"average minutes": time/len(res)})


@statistics_api_blueprint.route('/api/stat/<user_id>/average-time', methods=['GET'])
def get_average_time_by_user(user_id):
    res = Stat.query.filter(Stat.date_finished!=None, Stat.assignee_id==user_id).all()
    time = 0
    for row in res:
        date_format_str = '%Y-%m-%d %H:%M:%S.%f'
        start = datetime.strptime(str(row.to_json()['date_created']), date_format_str)
        end = datetime.strptime(str(row.to_json()['date_finished']), date_format_str)
        diff = end - start
        diff_in_minutes = diff.total_seconds() / 60
        time += diff.total_seconds() / 60
    result = "this user doesn't have worked on single task" if not res else time/len(res)
    return jsonify({"average minutes": result})

