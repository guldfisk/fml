import datetime
import subprocess

from boto3 import session

from configparser import ConfigParser

from fml import paths
from fml.backup.boto import MultipartUpload
from fml.notify import send_mail


_parser = ConfigParser()
_parser.read(paths.CONFIG_PATH)
_spaces_keys = _parser["SPACES"]
_db_keys = _parser["DB"]

MAILGUN_KEY = _parser["MAIL"]["mailgun_key"]
MAILGUN_DOMAIN = _parser["MAIL"]["mailgun_domain"]
EMAIL = _parser["MAIL"]["owner_email"]


def backup_db(mail: bool = False) -> str:
    key = f'fml/db-backups/{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.dmp'
    with MultipartUpload(
        client=session.Session().client(
            "s3",
            region_name=_spaces_keys["region"],
            endpoint_url=_spaces_keys["endpoint"],
            aws_access_key_id=_spaces_keys["spaces_public_key"],
            aws_secret_access_key=_spaces_keys["spaces_secret_key"],
        ),
        bucket="phdk",
        key=key,
    ) as out_file:
        s = subprocess.Popen(
            [
                "pg_dump",
                "--dbname={dialect}://{username}:{password}@{host}/{database}".format(
                    **_db_keys
                ),
                "-Fc",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        while True:
            chunk = s.stdout.read(1024)
            if not chunk and s.poll() is not None:
                break
            out_file.write(chunk)

        if s.poll() != 0:
            if mail:
                try:
                    error_message = s.stderr.read().decode("utf8")
                except Exception as e:
                    error_message = str(e)
                send_mail("FML DB backup failed :(", "error: " + error_message)
            raise Exception("pg_dump failed")

    return key


if __name__ == "__main__":
    print(backup_db())
