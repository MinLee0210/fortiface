from __future__ import annotations

import time
from typing import IO, Any, Dict, List, Union

import numpy as np
from deepface import DeepFace

from fortiface.common.utils import datetime_now
from fortiface.modules.base import BaseModule


class FaceAnalyze(BaseModule):
    def __init__(self, actions: List[str] = None, detector_backend: str = "opencv"):
        super().__init__(name="[fortiface |> face_analyze]")
        self.actions = actions or ["age", "gender", "race", "emotion"]
        self.detector_backend = detector_backend

    def execute(
        self, payload: Union[str, np.ndarray, IO[bytes]]
    ) -> List[Dict[str, Any]]:
        """
        Executes the face analysis pipeline.

        Args:
            payload (Union[str, np.ndarray, IO[bytes]]): The image input for face analysis.
                Can be a file path, a NumPy array, or a byte stream.

        Returns:
            List[Dict[str, Any]]: A list of analysis results, including predictions for actions.

        Raises:
            RuntimeError: If DeepFace fails to process the image.
        """
        try:
            start_time = time.time()

            # Execute face analysis with DeepFace
            actions = DeepFace.analyze(
                img_path=payload,
                actions=self.actions,
                detector_backend=self.detector_backend,
            )

            execution_time = time.time() - start_time
            self.logger.info(
                f"[{datetime_now()}] [{self.name}] Execution completed in {execution_time:.4f} seconds."
            )

            return actions

        except RuntimeError as re:
            error_message = f"[{datetime_now()}] [{self.name}] RuntimeError during execution: {str(re)}"
            self.logger.error(error_message)
            raise RuntimeError(error_message) from re

        except Exception as e:
            error_message = (
                f"[{datetime_now()}] [{self.name}] Unexpected error: {str(e)}"
            )
            self.logger.error(error_message)
            raise RuntimeError(error_message) from e
