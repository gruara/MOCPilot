import yaml

with open('/etc/MOC/config.yml', 'r') as f:
    yaml_in=yaml.load(f, Loader=yaml.FullLoader)

main_conf=yaml_in['Service']['config']
env=yaml_in['Service']['environment']

with open(main_conf, 'r') as f:
    yaml_in=yaml.load(f, Loader=yaml.FullLoader)

config=yaml_in['Environments'][env]

DB_USER=config['DB']['db user']
DB_PASSWORD=config['DB']['db password']

system_user_id=''
system_token=''

maximum_concurrency=config['Various']['maximum concurrency']

schedular_sleep_time=config['Timers']['schedular sleep time']
controller_sleep_time=config['Timers']['controller sleep time']
runner_sleep_time=config['Timers']['runner sleep time']

# life of token in minutes
TOKEN_EXPIRY=config['Timers']['token expiry']


LOGGING_LEVEL=config['Logging']['level']
LOGGING_FORMAT=config['Logging']['format']
LOGGING_FILE_WEB_SERVICES=config['Logging']['web services filename']
LOGGING_FILE_SCHEDULAR=config['Logging']['schedular log filename']
LOGGING_FILE_COTROLLER=config['Logging']['controller log filename']
LOGGING_FILE_RUNNER=config['Logging']['runner log filename']

WEB_SERVICE_URL='{}/{}/{}/'.format(config['Web Services']['common url'],config['Web Services']['verion'],config['Web Services']['name'])
    

