from __future__ import annotations

from pymilvus import MilvusClient

from fortiface.common.logging_config import setup_logger
from fortiface.core.config import settings

logger = setup_logger("[CoreConfig]")


class MilvusConnection:
    _instance: MilvusConnection = None

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of the class is created (thread-safe).
        """
        if not cls._instance:
            if not cls._instance:
                cls._instance = super(MilvusConnection, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        host: str = settings.MILVUS_HOST,
        port: str = settings.MILVUS_PORT,
    ):
        """
        Initialize the RegisterService instance.

        Args:
            host (str): Milvus server host.
            port (str): Milvus server port.
        """
        if not hasattr(
            self, "initialized"
        ):  # Avoid reinitializing in singleton pattern
            try:
                milvus_uri = f"http://{host}:{port}"
                self.milvus_client = MilvusClient(uri=milvus_uri)
                logger.info()
                self.initialized = True  # Mark as initialized
            except Exception as e:
                raise RuntimeError(f"Cannot connect to Milvus at {milvus_uri}: {e}")
