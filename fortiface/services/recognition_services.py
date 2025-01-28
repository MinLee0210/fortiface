from __future__ import annotations

from typing import IO, Any, Dict, List, Union

import numpy as np

from fortiface.common.utils import generate_random_key
from fortiface.core.config import settings
from fortiface.modules.face_analyze import FaceAnalyze
from fortiface.modules.face_embedding import FaceEmbedding
from fortiface.services.base import BaseService


class RecognitionSerivce(BaseService):
    def __init__(self, name: str):
        super().__init__(name=name)

    def recognize(self, payload: Union[str, np.ndarray, IO[bytes]]):
        pass
