from __future__ import annotations

import numpy as np
from pymilvus import MilvusClient

from fortiface.common.utils import generate_random_key
from fortiface.core.config import settings
from fortiface.schemas.vector_schemas import FACE_SCHEMAS, INDEX_PARAMS
from fortiface.services.base import BaseService


class RegisterService(BaseService):
    def __init__(
        self,
        name="RegiserService",
        host: str = settings.MILVUS_HOST,
        port: str = settings.MILVUS_PORT,
        collection_name: str = settings.MILVUS_COLLECTION,
        partition_name: str = settings.MILVUS_PARTITION,
        schema=FACE_SCHEMAS,
    ):
        super().__init__(name=name)
        try:
            milvus_uri = f"http://{host}:{port}"
            self.milvus_client = MilvusClient(uri=milvus_uri)
            self.logger.info(f"Connected to Milvus: {milvus_uri}")
        except Exception as e:
            raise RuntimeError(f"Cannot connect to Milvus at {milvus_uri}")

        self.collection_name = collection_name
        self.partition_name = partition_name
        self.schema = schema

        self.init_collection(collection_name=collection_name, schema=schema)
        self.create_partition(partition_name=partition_name)

    # C(ollection) level
    def init_collection(self, collection_name: str, schema):
        # Check if the collection exists
        if not self.milvus_client.has_collection(collection_name=collection_name):
            self.logger.info(
                f"Collection '{collection_name}' does not exist. Creating..."
            )
            self.milvus_client.create_collection(
                collection_name=collection_name,
                schema=schema,
                auto_id=False,
                enable_dynamic_fields=True,
                metric_type="IP",  # TODO: Change this approach to read from .yaml file
            )
            self.milvus_client.create_index(
                collection_name=collection_name, index_params=INDEX_PARAMS
            )
        else:
            self.logger.info(
                f"Collection '{collection_name}' already exists. Using existing collection."
            )
            self.milvus_client.create_index(
                collection_name=collection_name, index_params=INDEX_PARAMS
            )
        res = self.milvus_client.get_collection_stats(collection_name=collection_name)
        return res

    def create_partition(self, partition_name):
        self.milvus_client.load_collection(
            collection_name=self.collection_name, schema=self.schema
        )
        res = self.milvus_client.has_partition(
            collection_name=self.collection_name, partition_name=partition_name
        )
        self.logger.info(f"Collection has partition: {res}")

        if res is False:
            self.milvus_client.create_partition(
                collection_name=self.collection_name, partition_name=partition_name
            )
            res = self.milvus_client.has_partition(
                collection_name=self.collection_name, partition_name=partition_name
            )
        return res

    def drop_collection(self, collection_name: str):
        """Drop the collection."""
        try:
            self.milvus_client.drop_collection(collection_name=collection_name)
            self.logger.info(f"Dropped collection '{collection_name}'.")
            return {"success": True}
        except Exception as e:
            message = f"Error dropping collection '{collection_name}': {e}"
            self.logger.error(message)
            raise RuntimeError(message)

    # I(nstance) level
    def insert(self, *, data):
        """Create a new vector"""
        try:
            data = data.model_dump()
            data["id"] = generate_random_key()
            result = self.milvus_client.insert(
                collection_name=self.collection_name,
                partition_name=self.partition_name,
                data=data,
            )
            self.logger.info(
                f"Successully update entity to {data['fullname']} - {result}"
            )

            return {"success": True, "data": data}
        except Exception as e:
            message = f"Error get data: {e}"
            self.logger.error(message)
            return {
                "success": False,
                "detail": "Invalid data type, please check your input data",
            }

    def search(self, *, data, limit: int = 1, search_params: dict = None) -> list:
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

    def get_identity(self, *, identity_id: str) -> dict:
        """Get identity"""
        try:
            conditions = f'identity_id like "{identity_id}%"'
            results = self.milvus_client.query(
                collection_name=self.collection_name,
                partition_name=self.partition_name,
                filter=conditions,
                limit=1,
                output_fields=["*"],
            )
            self._convert_vectors_to_float(results=results)
            return {"success": True, "data": results}
        except Exception as e:
            message = f"Error get data: {e}"
            self.logger.error(message)
            return {
                "success": True,
                "detail": "Invalid data type, please check your input data",
            }

    def update_identity(self, *, identity_id: str, data) -> dict:
        """Update an instance based on its vector's ID."""
        try:
            data = data.model_dump()
            identity = self.get_identity(identity_id=identity_id).get("data")[0]
            identity["identity_id"] = data.get(
                "identity_id", identity.get("identity_id")
            )
            identity["fullname"] = data.get("fullname", identity.get("fullname"))
            identity["image_url"] = data.get("image_url", identity.get("image_url"))
            identity["metadata"] = data.get("metadata", identity.get("metadata"))
            self.milvus_client.upsert(
                collection_name=self.collection_name,
                partition_name=self.partition_name,
                data=identity,
            )
            self.logger.info(f"Successfully updated vector for ID {identity_id}.")
            return {"success": True, "data": identity}
        except Exception as e:
            message = f"Error updating vector for ID {identity_id}: {e}"
            self.logger.error(message)
            return {
                "success": False,
                "detail": f"Error updating vector for ID {identity_id}",
            }

    def delete_identity(self, *, identity_id: str) -> dict:
        """Delete data by primary keys."""
        try:
            conditions = f"identity_id in ['{identity_id}']"
            self.milvus_client.delete(
                collection_name=self.collection_name,
                partition_name=self.partition_name,
                filter=conditions,
            )
            self.logger.info(
                f"Deleted identity's ID {identity_id} from '{self.collection_name}'."
            )
            return {"success": True, "data": f"Delete id {identity_id}"}
        except Exception as e:
            message = f"Error delete data: {e}"
            self.logger.error(message)
            return {"success": False, "detail": "ID is wrongly typed or it not exists"}

    @staticmethod
    def _convert_vectors_to_float(results: list[dict]):
        """Convert vectors from list[np.float32] to list[float]."""
        for result in results:
            if "vector" in result and isinstance(result["vector"][0], np.float32):
                result["vector"] = [float(val) for val in result["vector"]]


register_service = RegisterService()
