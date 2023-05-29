import pathlib

import pytest


@pytest.fixture(scope="module")
def test_file() -> pathlib.Path:
    def f(file_name: str):
        return pathlib.Path(pathlib.Path.cwd() / "tests/test_data" / file_name)
    
    return f
