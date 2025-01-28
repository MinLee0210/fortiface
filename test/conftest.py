import cv2
import pytest
from deepface import DeepFace

TEST_IMAGE_PATH = "./temp/images/test_00.jpg"


@pytest.fixture
def load_test_image():
    """Fixture to load the test image."""
    img = cv2.imread(TEST_IMAGE_PATH)
    if img is None:
        pytest.fail(f"Failed to load image from {TEST_IMAGE_PATH}")
    return img


@pytest.fixture
def analyze_image():
    """Fixture to analyze the test image with DeepFace."""
    try:
        objs = DeepFace.analyze(
            img_path=TEST_IMAGE_PATH, actions=["age", "gender", "race", "emotion"]
        )
        return objs
    except Exception as e:
        pytest.fail(f"DeepFace.analyze failed: {e}")
