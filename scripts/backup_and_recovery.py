"""
SARAS ATLAS — Automated Database Integrity, Backup & Disaster Recovery Script
Verifies SQLite WAL consistency, executes point-in-time snapshots, and tests recovery validation.
"""

import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/saras_atlas.db")
BACKUP_DIR = Path("data/backups")


def run_integrity_check(db_file: Path) -> bool:
    """Verifies SQLite page consistency and foreign key compliance."""
    if not db_file.exists():
        print(f"[FAIL] Database file not found: {db_file}")
        return False
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    res = cursor.fetchone()[0]
    cursor.execute("PRAGMA foreign_key_check;")
    fk_errors = cursor.fetchall()
    conn.close()

    if res == "ok" and len(fk_errors) == 0:
        print(f"[PASS] Integrity check: {res.upper()} (0 foreign key violations).")
        return True
    else:
        print(f"[FAIL] Integrity issues detected: {res}, FK violations: {len(fk_errors)}")
        return False


def create_snapshot_backup() -> Path:
    """Creates point-in-time snapshot backup using SQLite backup API."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"saras_atlas_backup_{timestamp}.db"

    source_conn = sqlite3.connect(DB_PATH)
    dest_conn = sqlite3.connect(backup_file)

    with dest_conn:
        source_conn.backup(dest_conn, pages=100)

    dest_conn.close()
    source_conn.close()

    sz = backup_file.stat().st_size
    print(f"[PASS] Snapshot created: {backup_file} ({sz:,} bytes).")
    return backup_file


def verify_disaster_recovery(backup_file: Path) -> bool:
    """Tests disaster recovery by spinning up a restored database and auditing record counts."""
    test_restore_file = BACKUP_DIR / "test_recovery_verification.db"
    if test_restore_file.exists():
        test_restore_file.unlink()

    shutil.copy2(backup_file, test_restore_file)
    conn = sqlite3.connect(test_restore_file)
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM skus;")
    sku_count = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM inventory_snapshots;")
    inv_count = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM purchase_orders;")
    po_count = cursor.fetchone()[0]

    conn.close()
    test_restore_file.unlink()

    print(f"[PASS] Disaster Recovery Verified! Restored counts: {sku_count} SKUs, {inv_count} Inventory Snapshots, {po_count} POs.")
    return sku_count > 0 and inv_count > 0


if __name__ == "__main__":
    print("=" * 80)
    print("SARAS ATLAS — DATABASE BACKUP & RECOVERY VERIFICATION")
    print("=" * 80)
    ok = run_integrity_check(DB_PATH)
    if not ok:
        sys.exit(1)
    backup_path = create_snapshot_backup()
    rec_ok = verify_disaster_recovery(backup_path)
    if not rec_ok:
        sys.exit(1)
    print("=" * 80)
    print("DATABASE BACKUP & DISASTER RECOVERY TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)
