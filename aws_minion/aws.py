import datetime
import os
import time
from textwrap import dedent

AWS_CREDENTIALS_PATH = '~/.aws/credentials'


def parse_time(s: str) -> float:
    try:
        utc = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
        return utc - time.timezone
    except:
        return None


def format_time(dt: datetime.datetime=None) -> str:
    """
    >>> dt = datetime.datetime.utcnow(); (dt.timestamp() - time.timezone) - parse_time(format_time(dt))
    0.0
    """
    if not dt:
        dt = datetime.datetime.utcnow()
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def write_aws_credentials(key_id, secret, session_token=None):
    credentials_path = os.path.expanduser(AWS_CREDENTIALS_PATH)
    os.makedirs(os.path.dirname(credentials_path), exist_ok=True)
    credentials_content = dedent('''\
            [default]
            aws_access_key_id     = {key_id}
            aws_secret_access_key = {secret}
            ''').format(key_id=key_id, secret=secret, datetime=datetime.datetime.now())
    if session_token:
        # apparently the different AWS SDKs either use "session_token" or "security_token", so set both
        credentials_content += 'aws_session_token = {}\n'.format(session_token)
        credentials_content += 'aws_security_token = {}\n'.format(session_token)
    with open(credentials_path, 'w') as fd:
        fd.write(credentials_content)
