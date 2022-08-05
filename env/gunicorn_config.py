from os import environ as env
import multiprocessing

PORT = int(env.get("PORT", 80))
# DEBUG_MODE = int(env.get("DEBUG_MODE", 0))

# Gunicorn config
bind = ":" + str(PORT)
workers = 1 # multiprocessing.cpu_count() * 2 + 1
threads = 1 # 2 * multiprocessing.cpu_count()