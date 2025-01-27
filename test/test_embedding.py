from deepface import DeepFace


def test_deepface_embedding_structure(load_test_image):
    """Test the structure of the output embeddings."""
    img = load_test_image
    embedding_objs = DeepFace.represent(img_path=img)

    # Check that the result is a list
    assert isinstance(embedding_objs, list), "Embedding objects should be a list."

    # Ensure at least one face is detected
    assert len(embedding_objs) > 0, "No faces detected in the test image."

    # Check the structure of the first embedding object
    first_obj = embedding_objs[0]
    required_keys = {"embedding", "facial_area", "face_confidence"}
    assert isinstance(first_obj, dict), "Each embedding object should be a dictionary."
    assert required_keys.issubset(first_obj.keys()), (
        "Missing required keys in embedding object."
    )


def test_facial_area(load_test_image):
    """Test the facial area coordinates."""
    img = load_test_image
    embedding_objs = DeepFace.represent(img_path=img)

    first_obj = embedding_objs[0]
    facial_area = first_obj.get("facial_area")

    # Check that facial_area is a dictionary with valid coordinates
    assert isinstance(facial_area, dict), "Facial area should be a dictionary."
    for key in ["x", "y", "w", "h"]:
        assert key in facial_area, f"Missing '{key}' in facial area."
        assert isinstance(facial_area[key], int), (
            f"'{key}' in facial area should be an integer."
        )


def test_face_confidence(load_test_image):
    """Test the face confidence value."""
    img = load_test_image
    embedding_objs = DeepFace.represent(img_path=img)

    first_obj = embedding_objs[0]
    face_confidence = first_obj.get("face_confidence")

    # Check that face_confidence is a valid float between 0 and 1
    assert isinstance(face_confidence, (float, int)), (
        "Face confidence should be a float or integer."
    )
    assert 0.0 <= face_confidence <= 1.0, "Face confidence should be between 0 and 1."


def test_embedding_length(load_test_image):
    """Test the length of the embedding vector."""
    img = load_test_image
    embedding_objs = DeepFace.represent(img_path=img)

    first_obj = embedding_objs[0]
    embedding = first_obj.get("embedding")

    # Check that embedding is a list of floats with expected length
    assert isinstance(embedding, list), "Embedding should be a list."
    assert all(isinstance(x, float) for x in embedding), (
        "Embedding values should be floats."
    )
    assert len(embedding) > 0, "Embedding vector should not be empty."
