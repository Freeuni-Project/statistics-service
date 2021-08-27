import json
import time
import pika
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from application import db, create_app
from application.models import Stat
from run import app

print(' [*] Connecting *statistics-service* to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='stat_queue', durable=True)

print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    data = json.loads(body)

    if properties.content_type == 'new_ticket':
        try:
            print(data)
            stat = Stat()
            stat.project_id = data["project_id"]
            stat.user_id = data["assignee_id"]
            stat.ticket_id = data["id"]
            stat.ticket_status = data["status"]
            stat.project_status = "project_status"

            with app.app_context():
                db.session.add(stat)
                db.session.commit()
        except exc.SQLAlchemyError:
            pass


channel.basic_consume(queue='stat_queue', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()
channel.close()