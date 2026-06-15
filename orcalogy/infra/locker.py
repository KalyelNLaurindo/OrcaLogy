from typing import Any

from filelock import FileLock


class FileLockManager:
    """Wrapper manager for POSIX/Windows advisory file locking.

    Uses `filelock` to coordinate multi-process concurrency control
    on the ledger journal files.
    """

    def __init__(self, lock_file_path: str, timeout: float = 10.0) -> None:
        self.lock_file_path = lock_file_path
        self.timeout = timeout
        self._lock = FileLock(self.lock_file_path, timeout=self.timeout)

    def __enter__(self) -> "FileLockManager":
        self._lock.acquire()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._lock.release()
