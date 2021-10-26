__author__ = 'Hedius'
__license__ = 'GPLv3'

import threading
from typing import Dict


class SharedStorage:
    """
    Shared storage with lock for sharing data between nextcord and flask
    Singleton.
    Contains lock and data dict
    """
    _instance = None

    def __init__(self):
        """
        Only init once -> singleton
        """
        if self._instance:
            return
        self.lock = threading.Lock()
        self.data: Dict = {}

    def __new__(cls):
        if not cls._instance:
            instance = super(SharedStorage, cls).__new__(cls)
            instance.__init__()
            SharedStorage._instance = instance
        return SharedStorage._instance
