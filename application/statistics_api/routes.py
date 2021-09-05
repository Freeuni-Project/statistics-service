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


@statistics_api_blueprint.route('/api/stat/<project_id>/average-time', methods=['GET'])
def get_average_time(project_id):
    res = Stat.query.filter(Stat.date_finished!=None, Stat.project_id==project_id).all()
    time = 0
    for row in res:
        date_format_str = '%Y-%m-%d %H:%M:%S.%f'
        start = datetime.strptime(str(row.to_json()['date_created']), date_format_str)
        end = datetime.strptime(str(row.to_json()['date_finished']), date_format_str)
        diff = end - start
        diff_in_minutes = diff.total_seconds() / 60
        time += diff_in_minutes
    result = "there is not finished task to calculate average time" if not res else time/len(res)
    return jsonify({"avg_time": result})


@statistics_api_blueprint.route('/api/stat/<project_id>/user-average-time', methods=['GET'])
def get_average_time_by_user(project_id):
    user_id = request.json['user_id']
    res = Stat.query.filter(Stat.project_id==project_id, Stat.date_finished!=None, Stat.assignee_id==user_id,).all()
    time = 0
    for row in res:
        date_format_str = '%Y-%m-%d %H:%M:%S.%f'
        start = datetime.strptime(str(row.to_json()['date_created']), date_format_str)
        end = datetime.strptime(str(row.to_json()['date_finished']), date_format_str)
        diff = end - start
        diff_in_minutes = diff.total_seconds() / 60
        time += diff_in_minutes
    result = "this user doesn't have worked on single task" if not res else time/len(res)
    return jsonify({"avg_time": result})


@statistics_api_blueprint.route('/api/stat/<project_id>/user-ticket-num', methods=['GET'])
def get_ticket_number_by_user(project_id):
    user_id = request.json['user_id']
    res = Stat.query.filter(Stat.project_id==project_id, Stat.date_finished!=None, Stat.assignee_id==user_id).all()
    return jsonify({"ticket_num": len(res)})