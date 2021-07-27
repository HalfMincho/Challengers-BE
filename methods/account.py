from random import choices
from connector import MySQL
from typing import Union, Tuple
from passlib.hash import pbkdf2_sha512
from constants.account import pbkdf2_hash_rounds, pbkdf2_hash_salt_size
from constants.mail import password_reset_mail_body, password_change_mail_body, username_find_mail_body
import re
import uuid
import mailer


def get_uuid(username=None, email=None) -> Union[uuid.UUID, None]:
    if not isinstance(username, str):
        username = None
    if not isinstance(email, str):
        email = None

    if username is None and email is None:
        raise ValueError('Neither username or email must be provided as string.')

    sql = MySQL()
    if username is not None:
        ret = sql.query('SELECT uuid FROM account WHERE username LIKE %s', (username, ))
        if len(ret) == 1:
            return uuid.UUID(bytes=ret[0][0])

    if email is not None:
        ret = sql.query('SELECT uuid FROM account WHERE email LIKE %s', (email, ))
        if len(ret) == 1:
            return uuid.UUID(bytes=ret[0][0])

    return None


def check_duplicate_mail(address: str) -> bool:
    sql = MySQL()
    try:
        if sql.query('SELECT COUNT(*) FROM account WHERE email LIKE %s', (address, ))[0][0] == 0:
            return False
        else:
            return True
    except:
        return True


def issue_register_token(email: str) -> Union[str, None]:
    sql = MySQL()

    try:
        if sql.query("SELECT COUNT(*) FROM account WHERE email LIKE %s", (email,))[0][0] != 0:
            return None
        while True:
            token = ''.join(choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~()'!*:@,;", k=8))
            if sql.query('SELECT COUNT(*) FROM mail_verification WHERE token=%s', (token, ))[0][0] == 0:
                break

        sql.query('INSERT INTO mail_verification (token, email) VALUE (%s, %s)', (token, email, ))
    except:
        return None
    else:
        return token


def verify_register_token(email: str, token: str) -> bool:
    sql = MySQL()

    try:
        if sql.query('SELECT COUNT(*) FROM mail_verification WHERE token=%s AND email=%s AND used=0',
                     (token, email, ))[0][0] != 1:
            return False

        sql.query('UPDATE mail_verification SET used=1 WHERE token=%s', (token, ))
    except:
        return False
    else:
        return True


def register(name: str, email: str, username: str, password: str, affiliation: str, major: str,
             token: str) -> Tuple[bool, Union[str, None]]:
    sql = MySQL()
    user_uuid = uuid.uuid4()
    while True:
        if sql.query('SELECT COUNT(*) FROM account WHERE uuid=%s', (user_uuid.bytes, ))[0][0] == 0:
            break

    if not re.fullmatch(r'^([\x21-\x7e]{8,})$', password):
        return False, 'password_policy_mismatch'

    if sql.query('SELECT COUNT(*) FROM account WHERE email LIKE %s', (email, ))[0][0] != 0:
        return False, 'email_exists'
    elif len(email) > 255:
        return False, 'email_too_long'

    if sql.query('SELECT COUNT(*) FROM account WHERE username LIKE %s', (username, ))[0][0] != 0:
        return False, 'username_exists'
    elif len(username) > 100:
        return False, 'username_too_long'

    if len(name) > 255:
        return False, 'name_too_long'

    password = pbkdf2_sha512.hash(password, rounds=pbkdf2_hash_rounds, salt_size=pbkdf2_hash_salt_size)

    sql.transaction.start()

    try:
        sql.query('INSERT INTO account (uuid, email, username, password, name, affiliation, major)'
                  ' VALUE (%s, %s, %s, %s, %s, %s, %s)',
                  (user_uuid.bytes, email, username, password, name, affiliation, major, ))
        sql.query('DELETE FROM mail_verification WHERE token=%s', (token, ))

    except:
        sql.transaction.rollback()
        return False, 'exception_occurred'
    else:
        sql.transaction.commit()
        return True, None


def login(username: str, password: str) -> bool:
    sql = MySQL()

    pw_hash = sql.query('SELECT password FROM account WHERE username LIKE %s', (username, ))
    if len(pw_hash) != 1:
        return False

    return pbkdf2_sha512.verify(password, pw_hash[0][0])


def get_user_data(user_uuid: uuid.UUID) -> Union[dict, None]:
    sql = MySQL(dict_cursor=True)

    data = sql.query('SELECT uuid, email, username, name, affiliation, major, last_login FROM account WHERE uuid=%s',
                     (user_uuid.bytes, ))

    if len(data) != 1:
        return None
    else:
        data = data[0]
        data['uuid'] = str(uuid.UUID(bytes=data['uuid']))

        return data


def change_password(user_uuid: uuid.UUID, old_password: str, new_password: str) -> Tuple[bool, Union[str, None]]:
    sql = MySQL()

    old_pw_hash = sql.query('SELECT password FROM account WHERE uuid=%s', (user_uuid.bytes, ))
    if len(old_pw_hash) != 1:
        return False, 'user_does_not_exists'
    elif not pbkdf2_sha512.verify(old_password, old_pw_hash[0][0]):
        return False, 'old_password_does_not_match'

    if not re.fullmatch(r'^([\x21-\x7e]{8,})$', new_password):
        return False, 'password_policy_mismatch'

    if sql.query('SELECT COUNT(*) FROM account WHERE uuid=%s', (user_uuid.bytes, ))[0][0] != 1:
        return False, 'user_does_not_exists'

    new_password = pbkdf2_sha512.hash(new_password, rounds=pbkdf2_hash_rounds, salt_size=pbkdf2_hash_salt_size)

    sql.transaction.start()
    try:
        sql.query('UPDATE account SET password=%s WHERE uuid=%s', (new_password, user_uuid.bytes, ))
    except:
        sql.transaction.rollback()
        return False, 'exception_occurred'

    if not mailer.send_one(sql.query('SELECT email FROM account WHERE uuid=%s', (user_uuid.bytes, ))[0][0],
                           'GISTORY user', 'GISTORY: 비밀번호 변경 알림', password_change_mail_body):
        return False, 'sending_mail_failed'
    else:
        sql.transaction.commit()
        return True, None


def find_username(name: str, email: str) -> Tuple[bool, Union[str, None]]:
    if name is None or email is None:
        return False, 'no_required_args'

    sql = MySQL(dict_cursor=True)
    try:
        res = sql.query('SELECT username FROM account WHERE name=%s AND email=%s', (name, email, ))
        if len(res) == 1:
            username = res[0]['username']
        else:
            return False, 'user_does_not_exists'
    except:
        return False, 'exception_occurred'

    if not mailer.send_one(email, 'GISTORY user', 'GISTORY: 아이디 찾기 메일',
                           username_find_mail_body.format(name=name, username=username)):
        return False, 'sending_mail_failed'
    else:
        return True, None


def reset_password(name: str, email: str, username: str) -> Tuple[bool, Union[str, None]]:
    if name is None or email is None or username is None:
        return False, 'no_required_args'

    sql = MySQL()
    try:
        res = sql.query('SELECT uuid FROM account WHERE name=%s AND email=%s AND username=%s',
                        (name, email, username, ))
        if len(res) == 1:
            user_uuid = uuid.UUID(bytes=res[0][0])
        else:
            return False, 'user_does_not_exists'
    except:
        return False, 'exception_occurred'

    new_password = str(uuid.uuid4()).replace('-', '')[:8]

    sql.transaction.start()
    try:
        sql.query('UPDATE account SET password=%s WHERE uuid=%s',
                  (pbkdf2_sha512.hash(new_password, rounds=pbkdf2_hash_rounds, salt_size=pbkdf2_hash_salt_size),
                   user_uuid.bytes,))
    except:
        sql.transaction.rollback()
        return False, 'exception_occurred'

    try:
        sql.query('DELETE FROM token WHERE uuid=%s', (user_uuid.bytes,))
    except:
        sql.transaction.rollback()
        return False, 'exception_occurred'

    if not mailer.send_one(email, 'GISTORY user', 'GISTORY: 비밀번호 초기화 메일',
                           password_reset_mail_body.format(new_password=new_password)):
        sql.transaction.rollback()
        return False, 'sending_mail_failed'
    else:
        sql.transaction.commit()
        return True, None
