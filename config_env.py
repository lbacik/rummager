
from os import getenv

env_soapurl = 'RUMMAGER_SOAPURL'
env_soapurl_sender = 'RUMMAGER_SOAPURL_SENDER'
env_log_dir = 'RUMMAGER_LOGDIR'
env_mainloop_delay = 'RUMMAGER_MAINLOOP_DELAY'

if getenv(env_soapurl):
    soapurl = getenv(env_soapurl)

if getenv(env_soapurl_sender):
    soapurl_sender = getenv(env_soapurl_sender)

if getenv(env_log_dir):
    log_dir = getenv(env_log_dir)

if getenv(env_mainloop_delay):
    mainloop_delay = getenv(env_mainloop_delay)
