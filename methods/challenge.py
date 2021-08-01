import uuid
from typing import Union
from connector import MySQL
from constants import messages


def get_challenge_by_id(challenge: int = None) -> Union[uuid.UUID, None]:
    if challenge is None:
        raise ValueError('Challenge must be provided as integer.')

    sql = MySQL()
    ret = sql.query('SELECT uuid FROM challenge WHERE id=%s', (challenge,))
    if len(ret) != 1:
        return None

    return uuid.UUID(bytes=ret[0][0])


def get_challenge(challenge_id: int):
    sql = MySQL(dict_cursor=True)

    result = sql.query('SELECT id, submitter, category, name, auth_way, auth_day, auth_count_in_day, '
                       'start_at, end_at, cost, description, reg_date, views FROM challenge WHERE id=%s',
                       (challenge_id,))

    if len(result) == 0:
        return False, None

    result = result[0]
    result['submitter'] = str(uuid.UUID(bytes=result['submitter']))
    result['category'] = str(uuid.UUID(bytes=result['category']))

    sql.transaction.start()
    try:
        sql.query('UPDATE challenge SET views = views + 1 WHERE id=%s', (challenge_id,))
    except:
        sql.transaction.rollback()
    else:
        sql.transaction.commit()
        result['views'] += 1

    return True, result


def create_challenge(submitter, category, name, auth_way, auth_day, auth_count_in_day, start_at, end_at,
                     cost, title_image, description):
    sql = MySQL()

    test_uuid = uuid.uuid4()

    if (submitter is None or category is None or name is None or auth_way is None or auth_day is None or
            auth_count_in_day is None or start_at is None or end_at is None or cost is None or
            title_image is None or description is None):
        return False, messages.no_required_args, 400

    sql.transaction.start()
    try:
        sql.query('INSERT INTO challenge (uuid, submitter, category, name, auth_way, auth_day,'
                  'auth_count_in_day, cost, description) '
                  'VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                  (test_uuid.bytes, test_uuid.bytes, test_uuid.bytes, name, auth_way, auth_day,
                   auth_count_in_day, cost, description))
    except:
        sql.transaction.rollback()
        return False, messages.exception_occurred, 500
    else:
        inserted = sql.query('SELECT LAST_INSERT_ID()')[0][0]
        sql.transaction.commit()
        return True, inserted, 200


def delete_challenge(challenge_id: int):
    sql = MySQL()

    result = sql.query('SELECT id FROM challenge WHERE id=%s', challenge_id)

    if len(result) == 0:
        return False, messages.challenge_no_exists, 404

    sql.transaction.start()
    try:
        sql.query('DELETE FROM challenge WHERE id=%s', challenge_id)
    except:
        sql.transaction.rollback()
        return False, messages.exception_occurred, 403
    else:
        sql.transaction.commit()
        return True, None, 200


def get_popular_challenge():
    sql = MySQL(dict_cursor=True)

    popular_challenge_list = list(sql.query('SELECT id, submitter, category, name, '
                                            'auth_way, auth_day, auth_count_in_day, start_at, '
                                            'end_at, cost, description, reg_date, views FROM challenge '
                                            'ORDER BY views desc LIMIT 0, 10'))
    for challenge in popular_challenge_list:
        challenge['submitter'] = str(uuid.UUID(bytes=challenge['submitter']))
        challenge['category'] = str(uuid.UUID(bytes=challenge['category']))

    return True, popular_challenge_list


def get_recent_challenge():
    sql = MySQL(dict_cursor=True)

    recent_challenge_list = list(sql.query('SELECT id, submitter, category, name, auth_way, auth_day, '
                                           'auth_count_in_day, start_at, end_at, cost, description, '
                                           'reg_date, views FROM challenge ORDER BY reg_date desc LIMIT 0, 10'))

    for challenge in recent_challenge_list:
        challenge['submitter'] = str(uuid.UUID(bytes=challenge['submitter']))
        challenge['category'] = str(uuid.UUID(bytes=challenge['category']))

    return True, recent_challenge_list
