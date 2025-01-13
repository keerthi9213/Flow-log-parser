import csv
from collections import defaultdict

def load_lookup_table(file_path):
    """
    Load the lookup table and store mappings as a dictionary for efficient lookups.
    """
    lookup = defaultdict(list)
    with open(file_path, 'r', encoding='ascii') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['dstport'].strip().lower(), row['protocol'].strip().lower())
            lookup[key].append(row['tag'].strip().lower())
    return lookup

def parse_flow_logs(file_path, lookup):
    """
    Parse the flow log file and map each log entry to a tag based on the lookup table.
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0

    with open(file_path, 'r', encoding='ascii') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 14:  # Skip malformed lines
                continue
            
            dstport = parts[5].strip()
            protocol_num = parts[7].strip()
            
            # Map protocol numbers to names
            protocol_map = {'6': 'tcp', '17': 'udp', '1': 'icmp'}
            protocol = protocol_map.get(protocol_num, '').lower()

            if not protocol:  # Skip if protocol mapping is missing
                continue

            key = (dstport.lower(), protocol)
            tags = lookup.get(key)

            # Update tag counts and untagged count
            if tags:
                for tag in tags:
                    tag_counts[tag] += 1
            else:
                untagged_count += 1

            # Update port/protocol combination counts
            port_protocol_counts[key] += 1

    return tag_counts, port_protocol_counts, untagged_count

def write_output(tag_counts, port_protocol_counts, untagged_count, output_file):
    """
    Write the results to an output file in the required format.
    """
    with open(output_file, 'w', encoding='ascii') as file:
        # Write Tag Counts
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")
        file.write(f"Untagged,{untagged_count}\n\n")

        # Write Port/Protocol Combination Counts
        file.write("Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

if __name__ == "__main__":
    # File paths
    lookup_file = "lookup_table.csv"
    flow_logs_file = "flow_logs.txt"
    output_file = "output.txt"

    # Step 1: Load the lookup table
    lookup = load_lookup_table(lookup_file)

    # Step 2: Parse the flow logs and compute counts
    tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(flow_logs_file, lookup)

    # Step 3: Write the output
    write_output(tag_counts, port_protocol_counts, untagged_count, output_file)

    print(f"Processing complete. Results written to {output_file}.")
