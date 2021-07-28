from uuid import UUID
from connector import MySQL
from constants import messages


def add_challenge_to_basket(submitter: UUID, challenge: UUID):
    sql = MySQL()

    if challenge is None:
        return False, messages.no_required_args, 400

    sql.transaction.start()
    try:
        sql.query('INSERT INTO shopping_basket (account, challenge) VALUE  (%s, %s)',
                  (submitter.bytes, challenge.bytes))
    except:
        sql.transaction.rollback()
        return False, messages.exception_occurred, 500
    else:
        inserted = sql.query('SELECT LAST_INSERT_ID()')[0][0]
        sql.transaction.commit()
        return True, inserted, 200
