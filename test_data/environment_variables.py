from environs import Env

# Get variables in .env
env = Env()
env.read_env()
domain = env('DOMAIN')
db_settings = env.json('DB_SETTINGS')
login_info_0 = env.json('LOGIN_INFO_0')
login_info_1 = env.json('LOGIN_INFO_1')
login_info_2 = env.json('LOGIN_INFO_2')
