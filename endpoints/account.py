from flask import Blueprint
from methods import account, token
from constants import frontend_address
from . import is_api, cors_allow, protected
import mailer
import constants.mail
import constants.account
import constants.messages

account_blueprint = Blueprint('Account', __name__)


@account_blueprint.route('/issue-register-token', methods=['POST', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api(required_keys=['email'], input_type='json')
def issue_register_token(data):
    if account.check_duplicate_mail(data['email']):
        return {'error': 'duplicated_mail_verification_failed'}, 400
    token = account.issue_register_token(data['email'])
    if token is None:
        return {'error': 'token_generation_failed'}, 500

    if not mailer.send_one(data['email'], 'GISTORY user', 'GISTORY: 회원가입을 위한 메일 인증',
                           constants.mail.mail_verification_mail_body.format(token=token), "html"):
        return {'error': 'sending_mail_failed'}, 500
    else:
        return {'success': True}, 201


@account_blueprint.route('verify-token', methods=['GET', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api(required_keys=['token', 'email'])
def verify_register_token(data):
    if account.verify_register_token(data['email'], data['token']):
        return {'message': 'token_verified'}, 200
    else:
        return {'error': 'verify_token_failed'}, 500


@account_blueprint.route('/register', methods=['POST', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api(required_keys=['name', 'email', 'token', 'id', 'password', 'phone_number'], input_type='json')
def register(data):
    if not account.verify_register_token(data['email'], data['token']):
        return {'error': 'register_token_verification_failed'}, 400

    state, error_code = account.register(**data)

    if not state:
        return {'error': error_code}, (400 if error_code != 'exception_occurred' else 500)

    else:
        return {'registered': True}, 201


@account_blueprint.route('/login', methods=['POST', 'OPTIONS'])
@cors_allow()
@is_api(required_keys=['username', 'password'], input_type='json')
def login(data):
    if not account.login(**data):
        return {'error': 'authentication_failed'}, 403

    user_uuid = account.get_uuid(id=data['id'])

    if user_uuid is None:
        return {'error': 'authentication_failed'}, 403

    status, user_token = token.issue(user_uuid)

    if not status:
        return {'error': 'token_issue_failed'}, 500
    else:
        return {'token': user_token}, 200


@account_blueprint.route('/revoke', methods=['POST', 'OPTIONS'])
@cors_allow()
@is_api(required_keys=['token'], input_type='json')
@protected(verify=True)
def revoke(user_uuid, user_token, data):
    user_uuid_by_token = token.get_owner(user_token)
    if user_uuid != user_uuid_by_token:
        return {'error': 'no_permission'}, 403

    if token.revoke(data['token']):
        return {'success': True}, 200
    else:
        return {'error': 'token_revoke_failed'}, 500


@account_blueprint.route('/token_validate', methods=['GET', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api()
@protected()
def token_validate(user_uuid, user_token, data):
    if user_uuid is None:
        return {'error': 'no_permission'}, 403
    else:
        return {'success': True}, 200


@account_blueprint.route('/user_data', methods=['GET', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api()
@protected()
def get_userdata(user_uuid, user_token, data):
    user_uuid_by_token = token.get_owner(user_token)
    if user_uuid != user_uuid_by_token:
        return {'error': 'no_permission'}, 403

    data = account.get_user_data(user_uuid)
    if data is None:
        return {'error': 'exception_occurred'}, 500
    else:
        return data


@account_blueprint.route('/user_data/password', methods=['POST', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api(required_keys=['old_password', 'new_password'], input_type='json')
@protected(verify=True)
def change_password(user_uuid, user_token, data):
    result, error = account.change_password(user_uuid, **data)

    if not result:
        return {'error': error}, (500 if error == 'exception_occurred' or error == 'sending_mail_failed' else 400)
    else:
        return {'success': True}, 200


@account_blueprint.route('/find_username', methods=['POST', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api(required_keys=['name', 'email'], input_type='json')
def find_username(data):
    result, error = account.find_id(**data)

    if not result:
        return {'error': error}, (404 if error == 'user_does_not_exists' else 500)
    else:
        return {'success': True}, 200


@account_blueprint.route('/reset_password', methods=['POST', 'OPTIONS'])
@cors_allow(frontend_address)
@is_api(required_keys=['name', 'email', 'id'], input_type='json')
def reset_password(data):
    result, error = account.reset_password(**data)

    if not result:
        return {'error': error}, (500 if error == 'exception_occurred' else 404)
    else:
        return {'success': True}, 200
