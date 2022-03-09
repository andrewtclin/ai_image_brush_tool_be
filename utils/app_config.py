import logging
import env as app_env


# logger info
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_filename = app_env.LOG_FILENAME + '.log'


logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)

handler = logging.FileHandler(log_filename)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

def write_log(level, msg):
	if level == 'info':
		logger.info(msg)
	elif level == 'warning':
		logger.warning(msg)
	elif level == 'critical':
		logger.critical(msg)