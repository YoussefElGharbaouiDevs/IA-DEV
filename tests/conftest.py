from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def cadrage_dir(root: Path) -> Path:
    return root / "docs" / "cadrage"


@pytest.fixture(scope="session", autouse=True)
def api_test_keys():
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("API_KEYS", "test-client-key-123456:client,test-admin-key-123456:admin")
        patch.setenv("API_KEY", "test-client-key-123456")
        yield
