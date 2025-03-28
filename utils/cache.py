from flask_caching import Cache

cache = Cache()

# Initialisation du cache avec la configuration par défaut
def init_cache(app):
    
    cache.init_app(app)
    return cache
