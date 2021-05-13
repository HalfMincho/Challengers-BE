from uuid import UUID
from connector import MySQL


def get_challenge(challenge_id: int):
    sql = MySQL()

    result = sql.query('SELECT id, submitter, category, name, auth_way, auth_day, auth_count_in_day, '
                       'start_at, and_at, cost, description FROM challenge WHERE id=%s', (challenge_id,))

    if len(result) == 0:
        return False, None

    result = result[0]

    return True, result
