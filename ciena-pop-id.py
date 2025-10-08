from globalnoc import wsc
import getpass
import csv

# Change this if your KVP type is different
POP_KVP_TYPE_ID = 2

def main():
    # --- Credentials ---
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ").strip()
    if not username or not password:
        print("Username and password cannot be empty.")
        return

    # --- CSV path ---
    csv_path = input("Path to CSV (with 'POP ID' and 'Ciena Site ID'): ").strip()
    if not csv_path:
        print("CSV path is required.")
        return

    # --- Client setup ---
    client = wsc.WSC()
    client.username = username
    client.password = password
    client.url = <redacted>
    client.realm = <redacted>

    total = 0
    ok = 0
    errors = 0
    skipped = 0

    # --- Read and update per row ---
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Minimal header check. You would need to change this based on the KVP values you are updating
        for h in ("POP ID", "Ciena Site ID"):
            if h not in (reader.fieldnames or []):
                raise ValueError(f"CSV must include column '{h}'. Found: {reader.fieldnames}")

        for i, row in enumerate(reader, start=1):
            total += 1
            pop_id_raw = (row.get("POP ID") or "").strip()
            value = (row.get("Ciena Site ID") or "").strip()

            if not pop_id_raw or not value:
                skipped += 1
                print(f"[{i}] SKIP (missing data): POP ID='{pop_id_raw}', Ciena Site ID='{value}'")
                continue

            # Make sure POP IDs are numeric
            try:
                pop_id = int(pop_id_raw)
            except ValueError:
                pop_id = pop_id_raw  # allow non-numeric IDs too

            try:
                resp = client.add_pop_kvp(
                    pop_id=pop_id,
                    pop_kvp_type_id=POP_KVP_TYPE_ID,
                    value=value
                )
                if isinstance(resp, dict) and resp.get("error"):
                    errors += 1
                    print(f"[{i}] ERROR: {resp.get('error_text', resp)}")
                else:
                    ok += 1
                    print(f"[{i}] OK: pop_id={pop_id}, value={value}")
            except Exception as e:
                errors += 1
                print(f"[{i}] EXCEPTION for pop_id={pop_id}: {e}")

    print("\n=== Done ===")
    print(f"Total rows: {total} | OK: {ok} | Errors: {errors} | Skipped: {skipped}")

if __name__ == "__main__":
    main()
