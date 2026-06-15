import tempfile
from decimal import Decimal
from pathlib import Path

import pytest

from orcalogy.infra.parser import load_config


def test_load_config_success() -> None:
    # Arrange
    toml_content = """
    [settings]
    currency = "BRL"

    [limits]
    Food = 800.00
    Leisure = 300.50
    Transport = 200
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".toml") as tmp:
        tmp.write(toml_content)
        tmp_path = tmp.name

    try:
        # Act
        config = load_config(tmp_path)

        # Assert
        assert config.currency == "BRL"
        assert config.limits["Food"] == Decimal("800.00")
        assert config.limits["Leisure"] == Decimal("300.50")
        assert config.limits["Transport"] == Decimal("200.00")
    finally:
        Path(tmp_path).unlink()


def test_load_config_missing_sections() -> None:
    toml_content = """
    [settings]
    currency = "USD"
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".toml") as tmp:
        tmp.write(toml_content)
        tmp_path = tmp.name

    try:
        config = load_config(tmp_path)
        assert config.currency == "USD"
        assert config.limits == {}
    finally:
        Path(tmp_path).unlink()


def test_advisory_file_locking(tmp_path: Path) -> None:
    """Verify that FileLockManager prevents concurrent locking on the same resource."""
    import time
    from concurrent.futures import ThreadPoolExecutor

    from filelock import Timeout

    from orcalogy.infra.locker import FileLockManager

    lock_file = tmp_path / "ledger.lock"

    # 1. Verify exclusive acquisition
    lock1 = FileLockManager(str(lock_file), timeout=0.1)
    lock2 = FileLockManager(str(lock_file), timeout=0.1)

    with lock1:
        # lock1 holds the lock, lock2 should fail due to timeout
        with pytest.raises(Timeout):
            with lock2:
                pass

    # 2. Verify release allows subsequent acquisition
    with lock2:
        pass  # should succeed now that lock1 released it

    # 3. Verify thread-safety/queuing order
    shared_resource: list[int] = []

    def worker(worker_id: int, delay: float) -> None:
        lock = FileLockManager(str(lock_file), timeout=2.0)
        with lock:
            time.sleep(delay)
            shared_resource.append(worker_id)

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Worker 1 starts and holds lock for 0.2s
        f1 = executor.submit(worker, 1, 0.2)
        # Worker 2 tries to enter shortly after, must block and wait
        time.sleep(0.05)
        f2 = executor.submit(worker, 2, 0.01)

        f1.result()
        f2.result()

    # Worker 1 must have executed and appended first
    assert shared_resource == [1, 2]
