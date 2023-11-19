"""Logger configuration"""

from datetime import datetime
import logging
import os

from colorlog import ColoredFormatter


log = logging.getLogger()


def config_logging(log_directory=None, level=logging.INFO):
	"""
	Create logging configuration.

	1. Logging to file, if log_directory is specified. The log is more detailed than printed on screen.
	   Log file name includes date and time of log creation.
	2. Logging on screen
	"""
	if log_directory is not None:
		os.makedirs(log_directory, exist_ok=True)
		log_path = os.path.join(log_directory, "log_" + datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".txt")
		log.info(f"configuring logging to file {log_path}.")
	else:
		log_path = os.devnull

	for handler in logging.root.handlers[:]:
		logging.root.removeHandler(handler)

	# Configure logging to file
	logging.basicConfig(level=level, format="%(asctime)s %(levelname)-8s %(name)s %(funcName)s %(message)s",
						datefmt="%Y-%m-%d %H:%M:%S",
						filename=log_path,
						filemode="w")

	# Add a logging console
	console = logging.StreamHandler()
	console.setLevel(level)
	formatter = ColoredFormatter("%(log_color)s %(asctime)s %(levelname)-8s %(message)s",
								 datefmt="%Y-%m-%d %H:%M:%S",
								 reset=True,
								 log_colors={"DEBUG": "cyan",
								 			 "INFO": "blue",
								 			 "WARNING": "yellow",
								 			 "ERROR": "red",
								 			 "CRITICAL": "red, bg_white"},
								 secondary_log_colors={},
								 style="%")
	console.setFormatter(formatter)
	log.addHandler(console)

	log.info(f"Logger configured. Logging level: {logging.getLevelName(level)}")


config_logging()
