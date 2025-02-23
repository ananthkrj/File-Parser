# File-Parser

A program that can parse a file i.e: flow_logs.txt, containing flow log data and maps each row to a tag based on a lookup table i.e: lookup_table.csv. The produced output is stored in the example_output.txt file.

# How to Compile/Run the program

This program was written and ran with Python3 version 3.12. I will describe a few different methods of compiling and running this program based on whatever environment the user is working with.

If using VSCODE: 
- Simply copy paste link to github repository into vscodes git integration. 
- Once all file contents are loaded up, scrap the example_output.txt file so that it is blank.
- In the terminal run the command: python3 file_parser.py, and the output of the program will be copied into example_output.txt.
- To run the created tests for the program, type command: python3 test_file_parser.py in the terminal.

If using Linux/Unix Environment:
- Copy the SSH key of the repository and paste it following the git clone command in your terminal.
- Navigate into the project directory using command: cd repository-name
- Run the program: python3 file_parser.py
- Run the test file: python3 test_file_parser.py

# Program Tests

Test Setup and Teardown:
- SetUpClass: Creates temporary test files (test_lookup_table.csv and test_flow_logs.txt) for use in the tests.
- The test_lookup_table.csv file contains a small lookup table with the following mappings:

   (25, tcp) → sv_P1

   (443, tcp) → sv_P2

   (110, tcp) → email

- The test_flow_logs.txt file contains sample flow log entries that match the lookup table entries.
- tearDownClass: Cleans up the temporary test files after all tests are completed to ensure no leftover files.

The lookup table:
- Verify that the read_lookup_table function correctly reads the lookup table CSV file and converts it into a dictionary.
- The function reads the CSV file and creates a dictionary where the keys are tuples of (dstport, protocol) and the values are the corresponding tags.
- The test checks that the dictionary matches my expected structure.

Parsing the flow logs:
- Verify that the parse_flow_logs function correctly parses the flow log file and assigns tags based on the lookup table.
- The function processes each line in the flow log file, extracts the dstport and protocol fields, and assigns tags using the lookup table.
- Makes sure that tag counts and port/portocol combos match the expected values.

Copying Output:
- Verify that the copy_output function correctly writes the tag counts and port/protocol combination counts to the output file.

Edge Cases:
- test_empty_flow_log_file verifies that the program handles an empty flow log file correctly.
- test_empty_lookup_table_file verifies that the program handles an empty lookup table file correctly.

# Assumptions I Made

Default Log Format:
- Upon reading the AWS resource provided ensured that the sample flow log file follows the default log format (version 2).

lookup table and flow logs:
- I assumed a separate CSV file is required for storing the lookup table contents and I applied the same logic for the sample flow logs. 
- I could have technically included all of this information within file_parser.py but this would have came at a cost of code readibility and organization.

Supported Protocols:
- I assumed the only supported protocols were tcp (integer 6) and udp (integer 17).

Case Sensitivity:
- Made sure the program does not care about the capitilization of protocol names (e.g: tcp and TCP).

No Network Communication:
- While I realized this assessment revolves around the concept of network protocols and flows I still made sure that this program does not interact with any network resources. (e.g: The socket library in python).
- This ensured everything is ran on local files.

Error handling for Missing Files:
- While the assessment instructions state that sample flow log data and a lookup table will be present, made sure to take care of "deployment" cases where flow log or lookup table files could be empty.

Duplicate Keys:
- Program assumes that the lookup table does not contain duplicate (dstport, protocol) combinations. If duplicates exist, the last occurrence in the file will overwrite previous entries.

Validation of Input Data:
- Program assumes that the input data (e.g., dstport, protocol) is valid and does not perform additional validation (e.g., checking if dstport is a valid port number).

Incomplete Lines:
- To avoid a large test_file_parser.py file assumed that flow logs provided are not malinformed or incomplete. 
- An example case would be when flow log lines are fewer than 8 fields. I mainly did not incorporate this test case for the sake of time, however when it comes to actual deployment this case would definitely have importance as we may not control the sample flow log data provided.

# Analysis
- Completing this was a lot of fun in general, learned a lot about how crucial flow logs are important for network patterns, and can definitely see how they can tighten rules on security investigations.