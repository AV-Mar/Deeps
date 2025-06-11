import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise EnvironmentError('Required environment variables TELEGRAM_TOKEN and OPENROUTER_API_KEY are not set')
