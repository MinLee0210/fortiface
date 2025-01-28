from __future__ import annotations

from abc import ABC, abstractmethod
from typing import IO, Any, Dict, List, Union

import numpy as np

from fortiface.common.logging_config import setup_logger
from fortiface.core.supported_3rdparty import (FACE_ATTRIBUTES,
                                               FACE_DETECTION_MODELS,
                                               FACE_RECOGNITION_MODELS)


class BaseModule(ABC):
    def __init__(
        self,
        name: str = "fortiface",
        model_name: str = "VGG-Face",
        detector_backend: str = "opencv",
        actions: list = ["age", "gender", "race", "emotion"],
    ):
        self.logger = setup_logger(name)

        assert model_name in FACE_RECOGNITION_MODELS
        assert detector_backend in FACE_DETECTION_MODELS
        assert actions in FACE_ATTRIBUTES

        self.model_name = model_name
        self.detector_backend = detector_backend
        self.actions = actions

    @abstractmethod
    def execute(
        self, payload: Union[str, np.ndarray, IO[bytes]]
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError
