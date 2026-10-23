from importlib.metadata import version


def test_package_is_importable() -> None:
    import enterprise_ai_copilot

    assert enterprise_ai_copilot.__name__ == "enterprise_ai_copilot"


def test_distribution_metadata_is_available() -> None:
    assert version("enterprise-ai-copilot")
