from __future__ import annotations

import sys


def main() -> int:
    try:
        import pytest
    except Exception:
        sys.stderr.write("pytest 未安装。请先执行：uv sync --group dev\n")
        return 1

    return pytest.main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())

