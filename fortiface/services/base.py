"""
We have to type of servives: 
1. CRUD service for register. 
2. Inference for recognition: searching most familiar faces. 

As a result, the most abstract class for all of the services include: 
1. Logger. 
"""
from __future__ import annotations

from abc import ABC

from fortiface.common import setup_logger

class BaseService(ABC): 

    def __init__(self, name: str, *args, **kwargs): 
        self.logger = setup_logger(name)

