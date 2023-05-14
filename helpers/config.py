import yaml
import os

config_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

with open(f'{config_dir}/config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

LMS_URL = config['LMS_URL']
STUDIO_URL = config['STUDIO_URL']

STAFF_EMAIL = config['STAFF_EMAIL']
STAFF_PASSWORD = config['STAFF_PASSWORD']

REPORT_PATH = config['REPORT_PATH']
INSTANCE_NAME = config['INSTANCE_NAME']

REQUEST_BATCH_SIZE = config.get('REQUEST_BATCH_SIZE', 10)
