import csv
from pathlib import Path

# Your master list
role_codes = ['acp', 'agg', 'bastion', 'cld-perf', 'cndtr', 'colo', 'colo-srv', 'colo-sw', 'core', 'cpe-pbs', 'cpe-rtr', 'ctms', 'cube', 'cucm', 'dcn-sw', 'dcp', 'drawer', 'dtn-pas', 'dwdm', 'dwdm-noc', 'dwdmdcp', 'ext-rtr', 'fdp', 'fsfw', 'fw-node', 'fw-vip', 'geni', 'genisw', 'gnat', 'inverter', 'iss-pcap', 'iss-sw', 'iss-term', 'iss-vprd', 'k8s', 'kvm-rr', 'lan', 'lcsn-srv', 'mc', 'mcp', 'mfp', 'mitel-sw', 'mpo-fdp', 'mse', 'mse-b', 'mss', 'mssdcp', 'mtg-rtr', 'mvs', 'nddi-ctl', 'nddi-dev', 'nddi-sw', 'nms-nddi', 'nms-octr', 'nms-oexp', 'nms-othr', 'nms-rexp', 'nms-rlat', 'nms-rpho', 'nms-rpsv', 'nms-rthr', 'nso', 'obsacp', 'of', 'of-proxy', 'omea', 'ons-demo', 'ons-vm', 'oob', 'opncloud', 'opt', 'OSDF', 'pas', 'pas-tst', 'pdu', 'ps', 'rect', 'rr', 'rtr', 'rtr-pbs', 'rtrdcp', 'rtrng', 'rtsw', 'sdn-dcp', 'sdn-srv', 'sdn-sw', 'sip-mon', 'smn-fw', 'smn-rtsw', 'smn-term', 'spare', 'splitter', 'spp', 'sw', 'sw-fgn', 'syslog', 'testrtr', 'tray', 'ucs', 'ups', 'vcs', 'video-sw', 'vini', 'vs-srv', 'vs-sw', 'wave-sw', 'xena']

input_file  = "nodes.csv"
output_file = "unused_role_codes.csv"

# Case-insensitive mapping to preserve your original casing
role_codes_lower = {rc.lower(): rc for rc in role_codes}

def norm(h: str) -> str:
    return (h or "").strip().lower().replace(" ", "_")

inactive_statuses = {
    "decom", "decommissioned", "retired", "retired/decom",
    "decomm", "decommission", "inactive", "removed", "dead",
}

with open(input_file, newline="") as infile:
    reader = csv.DictReader(infile)
    headers = reader.fieldnames or []
    header_map = {norm(h): h for h in headers}

    # try to detect these automatically; adjust if you prefer hard-coded names
    role_key = header_map.get("role_code") or header_map.get("node_role_code") \
               or header_map.get("role") or header_map.get("node_role")
    status_key = header_map.get("status") or header_map.get("node_status") or header_map.get("state")

    if not role_key:
        raise KeyError(f"Couldn't find a role-code column in headers: {headers}")

    active_roles_present_lower = set()

    for row in reader:
        role_val = (row.get(role_key) or "").strip()
        status_val = (row.get(status_key) or "").strip() if status_key else ""

        # treat as active unless status is in the inactive set
        if role_val and status_val.lower() not in inactive_statuses:
            active_roles_present_lower.add(role_val.lower())

unused = [role_codes_lower[rc_l] for rc_l in role_codes_lower if rc_l not in active_roles_present_lower]

# write as a single-column CSV
with open(output_file, "w", newline="") as out:
    w = csv.writer(out)
    w.writerow(["unused_role_code"])
    for code in unused:
        w.writerow([code])

print(f"Active roles found: {len(active_roles_present_lower)}")
print(f"Unused role codes:  {len(unused)}")
