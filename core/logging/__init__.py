import json, sys, logging
from typing import Dict 
from loguru import logger
from pathlib import Path
from fastapi import FastAPI
from pydantic import Json

class InterceptHandler(logging.Handler):
    loglevel_map = {
        100: 'CRITICAL',
        80: 'ERROR',
        50: 'WARNING',
        30: 'INFO',
        15: 'DEBUG',
        0: 'NOTSET'
    }

    def emit(self, record):
        level = None
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_map[record.levelno]   
        
        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())

class CustomizeLogger:

    @classmethod
    def make_logger(cls, config_path: Path) -> logging.Logger:
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        logger = cls.customize_logging(
            logging_config.get('path'),
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=logging_config.get('format')
        )
        return logger
    
    @classmethod
    def customize_logging(cls,filepath: Path,level: str,rotation: str,retention: str,format: str ) -> logging.Logger:

        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        # may use hypercorn?
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


    @classmethod
    def load_logging_config(cls, config_path) -> None | Json:
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config

def register_logs(app: FastAPI) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger = CustomizeLogger.make_logger(
        Path(__file__).parent.resolve() / "config.json")
    app.logger = logger
    return logger