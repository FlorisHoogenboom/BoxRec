__all__ = ['data_acces' , 'services' , 'parsers', 'models']
BASE_URL = 'http://boxrec.com/en'

from . import services
from .services import FightServiceFactory