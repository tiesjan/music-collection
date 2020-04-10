try:
    # Attempt to import the build settings
    from .build import *  # noqa
except ImportError:
    # If the build settings cannot be found, import the base settings
    from .base import *  # noqa
