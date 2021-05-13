from uuid import UUID
from connector import MySQL
from constants import messages


def get_challenge(challenge_id: int):
    sql = MySQL()

    result = sql.query('SELECT id, submitter, category, name, auth_way, auth_day, auth_count_in_day, '
                       'start_at, end_at, cost, description FROM challenge WHERE id=%s', (challenge_id,))

    if len(result) == 0:
        return False, None

    result = result[0]

    return True, result


def create_challenge(submitter, category, name, auth_way, auth_day, auth_count_in_day, start_at, end_at,
                     cost, title_image, description):
    sql = MySQL()

    if (submitter is None or category is None or name is None or auth_way is None or auth_day is None or
            auth_count_in_day is None or start_at is None or end_at is None or cost is None or
            title_image is None or description):
        return False, messages.no_required_args, 400

    sql.transaction.start()
    try:
        sql.query('INSERT INTO challenge (submitter, category, name, auth_way, auth_day, auth_count_in_day, start_at, '
                  'end_at, cost, title_iamge, description) '
                  'VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                  (submitter, category, name, auth_way, auth_day, auth_count_in_day,
                   start_at, end_at, cost, title_image, description))
    except:
        sql.transaction.rollback()
        return False, messages.exception_occurred, 500
    else:
        inserted = sql.query('SELECT LAST_INSERT_ID()')[0][0]
        sql.transaction.commit()
        return True, inserted, 200
