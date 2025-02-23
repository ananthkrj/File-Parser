import csv
from collections import defaultdict

def read_lookup_table(lookup_file):
    """
    Reads the csv file lookup table.
    """
    lookup = {}
    with open(lookup_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['dstport'], row['protocol'].lower())
            lookup[key] = row['tag']
    return lookup


def parse_flow_logs(flow_log_file, lookup):
    """
    Parses the flow logs present 
    in the flow_logs.txt file.
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    protocol_map = {"6": "tcp", "17": "udp"}

    with open(flow_log_file, 'r') as f:
        for line in f: 
            parts = line.strip().split()
            if len(parts) < 8:
                continue

            dstport = parts[5]
            protocol = protocol_map.get(parts[7], parts[7]).lower()  # Convert if numeric

            key = (dstport, protocol)
            tag = lookup.get(key, 'Untagged')
            tag_counts[tag] += 1

            port_protocol_counts[key] += 1
    
    return tag_counts, port_protocol_counts

            
def copy_output(output_file, tag_counts, port_protocol_counts):
    """
    Copies the tag and port/protocol combination
    counts in an example output.txt file
    """
    with open(output_file, 'w') as f:
        untagged_count = tag_counts.pop("Untagged", None)

        f.write("Tag Counts:\n")
        f.write("Tag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            f.write(f"{tag},{count}\n")
        
        if untagged_count is not None:
            f.write(f"Untagged,{untagged_count}\n")
        
        f.write("Port/Protocol Combinations Counts:\n")
        f.write("Port,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            f.write(f"{port},{protocol},{count}\n")

def main(flow_log_file, lookup_file, output_file):
    """
    This is the main function
    """
    lookup = read_lookup_table(lookup_file)
    tag_counts, port_protocol_counts = parse_flow_logs(flow_log_file, lookup)
    copy_output(output_file, tag_counts, port_protocol_counts)

if __name__ == "__main__":
    flow_log_file = 'flow_logs.txt'
    lookup_file = 'lookup_table.csv'
    output_file = 'example_output.txt'
    main(flow_log_file, lookup_file, output_file)