# Flow Log Parser

## Project Overview
This project implements a parser for flow log data and maps each entry to tags based on a lookup table. The program:
1. Loads a lookup table (`lookup_table.csv`) with mappings of `dstport`, `protocol`, and `tag`.
2. Parses a flow log file (`flow_logs.txt`), extracting the `dstport` and `protocol`.
3. Maps each entry to a tag or marks it as "Untagged" if no match is found.
4. Outputs:
   - **Tag Counts**: Total matches for each tag.
   - **Port/Protocol Combination Counts**: Total occurrences of each `dstport` and `protocol` combination.

---

## How to Run
1. Prerequisites:
   - Python 3.6 or above.
   - Ensure `lookup_table.csv` and `flow_logs.txt` are in the same directory as `parse_flow_logs.py`.

2. Run the Script:
   python parse_flow_logs.py

Output File Format:

Tag Counts:
Tag,Count
sv_p1,15
email,10
sv_p2,5
Untagged,50

Port/Protocol Combination Counts:
Port,Protocol,Count
443,tcp,10
25,tcp,5
80,tcp,20

Generate Test Files:

Use random_files_gen.py to generate test files:
python random_files_gen.py

------------
Assumptions
Default AWS VPC Flow Log Format:

Supports only version 2.
Assumes all flow log entries are in the specified structure.
Case Insensitivity:

Matches dstport and protocol in a case-insensitive manner.

Dependencies:
Uses only Python’s standard library.

Testing
Sample Inputs:

lookup_table.csv: Includes mappings for various ports and protocols.
flow_logs.txt: Contains entries with:
Valid mappings (to test tagging logic).
Unmatched entries (to test "Untagged" functionality).

Test Coverage:
Case-insensitive matching for dstport and protocol.
Malformed lines in flow_logs.txt are ignored.
