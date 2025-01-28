from __future__ import annotations

import time
from typing import IO, Any, Dict, List, Union

import numpy as np
from deepface import DeepFace

from fortiface.common.utils import datetime_now
from fortiface.modules.base import BaseModule


class FaceEmbedding(BaseModule):
    def __init__(self, model_name: str = "DeepFace", detector_backend: str = "opencv"):
        """
        Initializes the FaceEmbedding module.

        Args:
            model_name (str): The model to use for embedding extraction (default is "DeepFace").
            detector_backend (str): The backend for face detection (default is "opencv").
        """
        super().__init__(name="[fortiface |> face_embedding]")
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

            # Extract face embeddings
            embedding = DeepFace.represent(
                payload,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
            )

            execution_time = time.time() - start_time
            self.logger.info(
                f"[{datetime_now()}] [{self.name}] Execution completed in {execution_time:.4f} seconds."
            )

            return embedding

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

    def _search(self, *, data, limit: int = 1, search_params: dict = None) -> list:
        """Search similar vectors"""
        if not search_params:
            search_params = {"metric_type": "IP"}

        try:
            data = data.model_dump()
            vector = data["vector"]
            results = self.milvus_client.search(
                collection_name=self.collection_name,
                partition_name=self.partition_name,
                data=[vector],
                limit=limit,
                params=search_params,
                output_fields=["*"],
            )
            self.logger.info(
                f"Search completed in collection '{self.collection_name}'."
            )
            return {"success": True, "data": results}
        except Exception as e:
            message = f"Error get data: {e}"
            self.logger.error(message)
            return {
                "success": False,
                "detail": "Invalid data type, please check your input data",
            }
