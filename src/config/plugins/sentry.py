import os

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN_KEY', ''),
    'environment': os.environ.get('NAMESPACE', ''),
    'site': 'Rehive',
}
