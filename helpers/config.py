import yaml
import os

config_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

with open(f'{config_dir}/config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

LMS_URL = config['LMS_URL']
STUDIO_URL = config['STUDIO_URL']

INSTANCE_NAME = config['INSTANCE_NAME']
