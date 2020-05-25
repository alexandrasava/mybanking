import logging
import logging.config


class Config:
    """Common configurations."""
    pass


class DevelopmentConfig(Config):
    """Development configurations."""

    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Disable CSRF to make curl testing easier.
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configurations."""
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


LOGGERS = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'mybanking.log',
            'formatter': 'default'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'mybanking': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG'
        },
        'default': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

logging.config.dictConfig(LOGGERS)
