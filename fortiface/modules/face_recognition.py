from __future__ import annotations

import time
from typing import IO, Any, Dict, List, Union

import numpy as np
from pymilvus import MilvusClient

from fortiface.common.utils import datetime_now
from fortiface.modules.base import BaseModule


class FaceRecognition(BaseModule):
    def __init__(self, model_name: str = "DeepFace", detector_backend: str = "opencv"):
        """
        Initializes the FaceRecognition module.

        Args:
            model_name (str): The model to use for embedding extraction (default is "DeepFace").
            detector_backend (str): The backend for face detection (default is "opencv").
        """
        super().__init__(name="[fortiface |> face_recognition]")
        self.model_name = model_name
        self.detector_backend = detector_backend

    def execute(
        self, payload: Union[str, np.ndarray, IO[bytes]]
    ) -> List[Dict[str, Any]]:
        """
        Executes face embedding extraction.

        Args:
            payload (Union[str, np.ndarray, IO[bytes]]): The image input for embedding extraction.
                Can be a file path, a NumPy array, or a byte stream.

        Returns:
            List[Dict[str, Any]]: A list of embeddings for the detected faces.

        Raises:
            RuntimeError: If DeepFace fails to process the image.
        """
        try:
            start_time = time.time()

            results = ...

            execution_time = time.time() - start_time
            self.logger.info(
                f"[{datetime_now()}] [{self.name}] Execution completed in {execution_time:.4f} seconds."
            )

            return results

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
