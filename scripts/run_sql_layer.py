"""Execute the Phase 3 DuckDB SQL layer from the repository root."""

from __future__ import annotations

import json
import os
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "sql"
DB_PATH = ROOT / "data" / "processed" / "ecommerce.duckdb"


def run_sql_layer(db_path: Path = DB_PATH) -> list[dict]:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    os.chdir(ROOT)
    connection = duckdb.connect(str(db_path))
    summaries: list[dict] = []
    try:
        for sql_path in sorted(SQL_DIR.glob("*.sql")):
            result = connection.execute(sql_path.read_text(encoding="utf-8"))
            try:
                frame = result.fetchdf()
                summary = {"file": sql_path.name, "rows": int(len(frame)), "columns": list(frame.columns)}
            except duckdb.NoResultException:
                summary = {"file": sql_path.name, "rows": 0, "columns": []}
            summaries.append(summary)
    finally:
        connection.close()
    return summaries


if __name__ == "__main__":
    output = run_sql_layer()
    print(json.dumps(output, indent=2))
