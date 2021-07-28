from flask import Blueprint
from methods import shopping_basket, challenge
from . import is_api, protected

shopping_basket_blueprint = Blueprint('Shopping_basket', __name__)


@shopping_basket_blueprint.route('', methods=['POST', 'OPTIONS'])
@is_api(required_keys=['challenge'], input_type='json')
@protected()
def add_challenge_to_basket(user_uuid, user_token, data):
    data['submitter'] = user_uuid
    data['challenge'] = challenge.get_challenge_by_id(data['challenge'])

    if data['challenge'] is None:
        return {'error': 'no_such_challenge'}, 404
    status, message, status_code = shopping_basket.add_challenge_to_basket(**data)

    if not status:
        return {'error': message}, status_code

    else:
        return {"created": message}