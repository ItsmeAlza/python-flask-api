from flask import request
from flask_restful import Resource
from flask_mail import Message
from app.extensions import mail
from app.utils.response import success_response, error_response

class SendEmail(Resource):
    def post(self):
        data = request.get_json()

        required_fields = ['to', 'subject', 'body']
        if not all(field in data for field in required_fields):
            return error_response("Missing required fields: to, subject, body", 400)

        msg = Message(
            subject=data['subject'],
            recipients=[data['to']],
            body=data['body']
        )

        try:
            mail.send(msg)
            return success_response(message="Email sent successfully")
        except Exception as e:
            return error_response(str(e), 500)
