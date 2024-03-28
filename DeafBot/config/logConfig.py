import logging
# Configure logging with a rotating file handler and different levels
logging_config = {
    'level': logging.INFO,  # Default log level (can be DEBUG for detailed logs)
    'filename': 'discord.log',
    'filemode': 'a',  # Use 'a' for appending to existing logs
    'format': 'Time: %(asctime)s \n- Name: %(name)s \n- Level: %(levelname)s \n- Message: %(message)s',
}