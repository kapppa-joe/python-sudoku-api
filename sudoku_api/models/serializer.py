import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from flask_marshmallow import Marshmallow

ma = Marshmallow()


def configure_marshmallow(app):
    ma.init_app(app)
    return ma
