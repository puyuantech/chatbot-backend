from flask import Blueprint
from flask_restful import Api
from .view import EvaluationAPI, EvalExplanation, EvalQuestion

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/eval')
api = Api(blu)

api.add_resource(EvaluationAPI, '/')
api.add_resource(EvalExplanation, '/explanations')
api.add_resource(EvalQuestion, '/questions')

