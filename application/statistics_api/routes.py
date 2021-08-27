# application/statistics_api/routes.py

from . import statistics_api_blueprint
from .. import db
from ..models import Stat
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

