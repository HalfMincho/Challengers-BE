from flask import Blueprint
from methods import challenge
from . import is_api
import constants.messages

challenge_blueprint = Blueprint('Challenge', __name__)


@challenge_blueprint.route('/<int:challenge_id>', methods=['GET', 'OPTIONS'])
@is_api()
def get_challenge(data, challenge_id: int):
    status, challenge_dict = challenge.get_challenge(challenge_id)

    if not status:
        return {'error': constants.messages.challenge_no_exists}, 404

    return challenge_dict


@challenge_blueprint.route('', methods=['POST', 'OPTIONS'])
@is_api()
def create_challenge(data):
    status, message, status_code = challenge.create_challenge(**data)

    if not status:
        return {'error': message}, status_code

    else:
        return {'created': message}