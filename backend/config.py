"""
Configuration settings for Quantum Battleship Backend
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'quantum-battleship-secret-key-2025')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # Game settings
    BOARD_SIZE = 10
    ENABLE_QUANTUM_MODE = True

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    # Quantum settings
    QUANTUM_BACKEND = 'aer_simulator'
    QUANTUM_SHOTS = 1024


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env='default'):
    """Get configuration based on environment"""
    return config.get(env, config['default'])