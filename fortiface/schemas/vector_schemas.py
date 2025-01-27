from pymilvus import CollectionSchema, DataType, FieldSchema, MilvusClient

FACE_FIELDS = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=256, is_primary=True),
    FieldSchema(
        name="vector",
        dtype=DataType.FLOAT_VECTOR,
        dim=512,
        description="A vector representation of a person's face",
    ),
    FieldSchema(
        name="fullname",
        dtype=DataType.VARCHAR,
        max_length=256,
        description="A fullname of a person",
    ),
    FieldSchema(
        name="image_url",
        dtype=DataType.VARCHAR,
        max_length=1024,
        description="Path to image (s3 storage, local storage, ...)",
    ),
    FieldSchema(
        name="metadata",
        dtype=DataType.JSON,
        description="Additional information of a person",
    ),
    FieldSchema(name="created_at", dtype=DataType.INT32),
    FieldSchema(name="modified_at", dtype=DataType.INT32),
]

FACE_SCHEMAS = CollectionSchema(fields=FACE_FIELDS)


INDEX_PARAMS = MilvusClient.prepare_index_params()


INDEX_PARAMS.add_index(
    field_name="vector",
    index_name="vector_index",
    index_type="AUTOINDEX",
    metric_type="IP",
)
