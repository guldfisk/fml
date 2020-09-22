import os

import appdirs

from secretresources import paths as _paths


APP_DATA_PATH = appdirs.AppDirs('fml', 'fml').user_data_dir

SECRETS_PATH = _paths.project_name_to_secret_dir('fml')

CONFIG_PATH = os.path.join(
    SECRETS_PATH,
    'config.cfg',
)

DB_PATH = os.path.join(APP_DATA_PATH, 'fml_2.db')

RESOURCE_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'resources',
)
