"""Classification d'avis français, modèle inclus dans la distribution."""
from importlib.metadata import version

from .predict import predict

__version__ = version("sentiment-app")
__all__ = ["predict", "__version__"]
