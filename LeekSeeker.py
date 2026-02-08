import argparse
import os

# Setup Argument Parser
parser = argparse.ArgumentParser(description="LeakSeeker - Search for breaches by domain")
parser.add_argument("domain", help="The domain to search for (e.g., @gmail.com)")
parser.add_argument("file", help="Path to the file containing breached data")
parser.add_argument("-o", "--output", help="Optional: File to save the results to")

args = parser.parse_args()

# Open the output file if provided
output_file = None
if args.output:
    if not os.path.exists(args.output):
        print(f"[*] Output file '{args.output}' doesn't exist.\n[*] Creating \"{args.output}\"...")
    else:
        print(f"[*] Output file '{args.output}' found. Overwriting content...")
        
    output_file = open(args.output, 'w', encoding='utf-8')
domains = args.domain.strip().split("|")

# Initialize dictionary to store results for each domain
results = {domain: [] for domain in domains}

try:
    with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
        print(f"[*] Searching for {', '.join(domains)} in {args.file}...")
        print("[*] Buffering results to sort by category... (Please wait)\n")
        
        for line in f:
            # Check if ANY of the domains are in the line
            for domain in domains:
                if domain in line:
                    results[domain].append(line.strip())
                    break # Stop checking other domains for this line

    # After scanning, print and write the results sorted by category
    for domain in domains:
        header = f"\n--- {domain} ---"
        print(header)
        
        if output_file:
            output_file.write(header + "\n")

        if results[domain]: # Only process if matches were found for this domain
            for line in results[domain]:
                print(line)
                if output_file:
                    output_file.write(line + "\n")
        else:
            print("No results found.")
            if output_file:
                output_file.write("No results found.\n")
            

except FileNotFoundError:
    print("Error: File not found!")
finally:
    # Close the output file if it was opened
    if output_file:
        output_file.close()
        if args.output:
            print(f"\n[+] Results saved to {args.output}")