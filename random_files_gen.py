import random
import string
import os

def generate_lookup_table(file_path, num_entries=5000):
    """
    Generate a lookup table with the specified number of mappings.
    """
    protocols = ['tcp', 'udp', 'icmp']
    tags = ['sv_P1', 'sv_P2', 'sv_P3', 'email', 'sv_P4', 'sv_P5']
    used_combinations = set()

    with open(file_path, 'w', newline='', encoding='ascii') as file:
        file.write("dstport,protocol,tag\n")  # Write header
        for _ in range(num_entries):
            dstport = random.randint(1, 65535)
            protocol = random.choice(protocols)
            tag = random.choice(tags)

            # Ensure unique port/protocol combinations
            while (dstport, protocol) in used_combinations:
                dstport = random.randint(1, 65535)
                protocol = random.choice(protocols)

            used_combinations.add((dstport, protocol))
            file.write(f"{dstport},{protocol},{tag}\n")

def generate_flow_logs(file_path, lookup_table, max_size=5 * 1024 * 1024):
    """
    Generate a flow log file with a size close to max_size (in bytes).
    """
    entries = []
    protocols = {'tcp': 6, 'udp': 17, 'icmp': 1}

    # Read lookup table to extract valid port/protocol combinations
    valid_combinations = []
    with open(lookup_table, 'r', encoding='ascii') as file:
        next(file)  # Skip header
        for line in file:
            dstport, protocol, _ = line.strip().split(',')
            valid_combinations.append((dstport, protocol))

    # Generate log entries until file size is reached
    current_size = 0
    with open(file_path, 'w', encoding='ascii') as file:
        while current_size < max_size:
            version = 2
            account_id = "123456789012"
            eni = f"eni-{random.randint(1000, 9999):04x}"
            srcaddr = f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"
            dstaddr = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
            srcport = random.randint(1024, 65535)

            dstport, protocol = random.choice(valid_combinations)
            protocol_num = protocols[protocol]
            packets = random.randint(1, 100)
            bytes_ = random.randint(1000, 100000)
            start = random.randint(1620000000, 1629999999)
            end = start + random.randint(10, 100)
            action = random.choice(['ACCEPT', 'REJECT'])
            log_status = "OK"

            log_entry = (
                f"{version} {account_id} {eni} {srcaddr} {dstaddr} "
                f"{dstport} {srcport} {protocol_num} {packets} {bytes_} "
                f"{start} {end} {action} {log_status}\n"
            )

            # Write log entry and update file size
            file.write(log_entry)
            current_size += len(log_entry)

    print(f"Flow log file generated: {file_path}, Size: {os.path.getsize(file_path)} bytes")

# File paths
lookup_file = "lookup_table.csv"
flow_log_file = "flow_logs.txt"

# Generate lookup table with 5000 mappings
generate_lookup_table(lookup_file, num_entries=5000)

# Generate flow logs with a file size close to 5 MB
generate_flow_logs(flow_log_file, lookup_table=lookup_file, max_size=5 * 1024 * 1024)

print(f"Lookup table generated: {lookup_file}, Entries: 5000")
