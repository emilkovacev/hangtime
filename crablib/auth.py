import bcrypt

from crablib.http.parse import Request
from db.account import get_account_from_token


def get_request_account(request: Request):
    if request.cookies and 'auth_token' in request.cookies:
        salt = b'$2b$12$Fr9yR03IQLCGqjB1MJ9gfu'
        auth_token_hash: str = bcrypt.hashpw(request.cookies['auth_token'].encode(), salt).decode()
        account = get_account_from_token(auth_token_hash)

        if account and account['auth_token_hash'] == auth_token_hash:
            return account
        return None

    return None
