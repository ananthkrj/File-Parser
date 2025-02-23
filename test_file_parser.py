import unittest
import os
import csv
from collections import defaultdict
from file_parser import read_lookup_table, parse_flow_logs, copy_output

class TestFileParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create temporary test files for lookup table and flow logs.
        """
        cls.lookup_file = 'test_lookup_table.csv'
        cls.flow_log_file = 'test_flow_logs.txt'
        cls.output_file = 'test_output.txt'

        # Create a test lookup table CSV file
        with open(cls.lookup_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['dstport', 'protocol', 'tag'])
            writer.writerow(['25', 'tcp', 'sv_P1'])
            writer.writerow(['443', 'tcp', 'sv_P2'])
            writer.writerow(['110', 'tcp', 'email'])

        # Create a test flow log file
        with open(cls.flow_log_file, 'w') as f:
            f.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
            f.write("2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 25 49154 6 15 12000 1620140761 1620140821 REJECT OK\n")
            f.write("2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 110 49155 6 10 8000 1620140761 1620140821 ACCEPT OK\n")
            f.write("2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 1024 49156 6 12 9000 1620140761 1620140821 ACCEPT OK\n")

    @classmethod
    def tearDownClass(cls):
        """
        Clean up temporary test files.
        """
        os.remove(cls.lookup_file)
        os.remove(cls.flow_log_file)
        os.remove(cls.output_file)

    def test_read_lookup_table(self):
        """
        Test if the lookup table is read correctly.
        """
        lookup = read_lookup_table(self.lookup_file)
        expected_lookup = {
            ('25', 'tcp'): 'sv_P1',
            ('443', 'tcp'): 'sv_P2',
            ('110', 'tcp'): 'email'
        }
        self.assertEqual(lookup, expected_lookup)

    def test_parse_flow_logs(self):
        """
        Test if the flow logs are parsed correctly.
        """
        lookup = read_lookup_table(self.lookup_file)
        tag_counts, port_protocol_counts = parse_flow_logs(self.flow_log_file, lookup)

        # Expected tag counts
        expected_tag_counts = defaultdict(int, {
            'sv_P2': 1,
            'sv_P1': 1,
            'email': 1,
            'Untagged': 1
        })
        self.assertEqual(tag_counts, expected_tag_counts)

        # Expected port/protocol counts
        expected_port_protocol_counts = defaultdict(int, {
            ('443', 'tcp'): 1,
            ('25', 'tcp'): 1,
            ('110', 'tcp'): 1,
            ('1024', 'tcp'): 1
        })
        self.assertEqual(port_protocol_counts, expected_port_protocol_counts)

    def test_copy_output(self):
        """
        Test if the output file is generated correctly.
        """
        lookup = read_lookup_table(self.lookup_file)
        tag_counts, port_protocol_counts = parse_flow_logs(self.flow_log_file, lookup)
        copy_output(self.output_file, tag_counts, port_protocol_counts)

        # Read the output file and verify its contents
        with open(self.output_file, 'r') as f:
            output = f.read()

        expected_output = (
            "Tag Counts:\n"
            "Tag,Count\n"
            "email,1\n"
            "sv_P1,1\n"
            "sv_P2,1\n"
            "Untagged,1\n"
            "Port/Protocol Combinations Counts:\n"
            "Port,Protocol,Count\n"
            "1024,tcp,1\n"
            "110,tcp,1\n"
            "25,tcp,1\n"
            "443,tcp,1\n"
        )
        self.assertEqual(output, expected_output)
    
    def test_empty_flow_log_file(self):
        """
        Test parsing an empty flow log file.
        """
        empty_flow_log_file = 'empty_flow_logs.txt'
        with open(empty_flow_log_file, 'w') as f:
            pass  # Create an empty file

        lookup = read_lookup_table(self.lookup_file)
        tag_counts, port_protocol_counts = parse_flow_logs(empty_flow_log_file, lookup)

        # Expected output: No tags or port/protocol combinations
        self.assertEqual(tag_counts, defaultdict(int))
        self.assertEqual(port_protocol_counts, defaultdict(int))

        os.remove(empty_flow_log_file)
    
    def test_empty_lookup_table_file(self):
        """
        Test reading an empty lookup table file.
        """
        empty_lookup_file = 'empty_lookup_table.csv'
        with open(empty_lookup_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['dstport', 'protocol', 'tag'])  # Header only

        lookup = read_lookup_table(empty_lookup_file)
        self.assertEqual(lookup, {})

        os.remove(empty_lookup_file)

if __name__ == "__main__":
    unittest.main()
