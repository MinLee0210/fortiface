def test_analyze_output_structure(analyze_image):
    """Test the structure of the analysis output."""
    objs = analyze_image

    # Check that the result is a list
    assert isinstance(objs, list), "The output should be a list."

    # Check that the first object in the list is a dictionary
    assert isinstance(objs[0], dict), "Each analysis result should be a dictionary."

    # Required keys in the analysis result
    required_keys = {"age", "gender", "race", "emotion"}
    assert required_keys.issubset(objs[0].keys()), (
        "Missing required keys in analysis result."
    )


def test_age_value(analyze_image):
    """Test that the age value is within a reasonable range."""
    objs = analyze_image
    age = objs[0].get("age")

    # Ensure age is an integer and within a reasonable range
    assert isinstance(age, (int, float)), "Age should be an integer or float."
    assert 0 <= age <= 120, "Age value is out of expected range (0-120)."


def test_gender_value(analyze_image):
    """Test that the gender value is valid."""
    objs = analyze_image
    gender = objs[0].get("gender")

    # Ensure gender prediction exists and is valid
    assert isinstance(gender, dict), "Gender should be a dictionary."
    assert "Woman" in gender or "Man" in gender, (
        "Gender keys should include 'Woman' or 'Man'."
    )

    # Gender probabilities should sum to 1 (or close due to floating-point precision)
    total_prob = sum(gender.values())
    assert abs(total_prob - 1.0) < 1e-3, "Gender probabilities should sum to 1."


def test_race_value(analyze_image):
    """Test that the race values are valid and probabilities sum to 1."""
    objs = analyze_image
    race = objs[0].get("race")

    # Ensure race prediction exists and is valid
    assert isinstance(race, dict), "Race should be a dictionary."
    assert len(race) > 0, "Race predictions should not be empty."

    # Probabilities should sum to 1 (or close due to floating-point precision)
    total_prob = sum(race.values())
    assert abs(total_prob - 1.0) < 1e-3, "Race probabilities should sum to 1."


def test_emotion_value(analyze_image):
    """Test that the emotion values are valid and probabilities sum to 1."""
    objs = analyze_image
    emotion = objs[0].get("emotion")

    # Ensure emotion prediction exists and is valid
    assert isinstance(emotion, dict), "Emotion should be a dictionary."
    assert len(emotion) > 0, "Emotion predictions should not be empty."

    # Probabilities should sum to 1 (or close due to floating-point precision)
    total_prob = sum(emotion.values())
    assert abs(total_prob - 1.0) < 1e-3, "Emotion probabilities should sum to 1."
