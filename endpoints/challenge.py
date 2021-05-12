from flask import Blueprint
from methods import challenge

challenge_blueprint = Blueprint('Challenge', __name__)


@challenge_blueprint.route('/<int:challenge_id>', methods=['GET', 'OPTIONS'])
def get_challenge(challenge_id: int):
    challenge_dict = challenge.get_challenge(challenge_id)

    return challenge_dict

