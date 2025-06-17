from .settings import *

# Override database host for local development
DATABASES["default"]["HOST"] = "localhost"
