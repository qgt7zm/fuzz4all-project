# Table 2: Fuzz4All models comparison (project version)
import argparse

def grab_csv_data(csv_file):
    import csv
    from collections import defaultdict
    import statistics as st

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        #headers = reader.fieldnames
        data = [row for row in reader]
        #print(headers)
        print(data)

    # Aggregate rows by target and fuzzer
    aggregated = defaultdict(lambda: defaultdict(lambda: [[], [], []]))
    for row in data:
        target = row["target"]
        fuzzer = row["model"]
        programs = int(row["count"])
        coverage = int(row["coverage"])
        valid = int(row["valid"])
        valid_percent = round(valid / programs * 100, 2)
        aggregated[target][fuzzer][0].append(programs)
        aggregated[target][fuzzer][1].append(coverage)
        aggregated[target][fuzzer][2].append(valid_percent)
    print(aggregated)

    # Average num programs, line coverage, and valid %
    ret_rows = []
    for target, tools in aggregated.items():
        for tool_name, trials in tools.items():
            avg_progs = str(int(st.mean(trials[0])))
            avg_cov = str(int(st.mean(trials[1])))
            avg_valid = str(round(st.mean(trials[2]), 2)) + "%"

            ret_rows.append([target, tool_name, avg_progs, avg_valid, avg_cov])

    return ret_rows


def rich_print(rows):
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(
        show_header=True,
        header_style="bold magenta",
        title="Fuzz4All against state-of-the-art fuzzers",
    )

    table.add_column("Target", style="dim", no_wrap=True)
    table.add_column("Fuzzer", justify="right", style="bold green")
    table.add_column("# programs", justify="right", style="bold blue")
    table.add_column("% valid", justify="right", style="bold blue")
    table.add_column("Coverage", justify="right", style="bold blue")

    for row in rows:
        table.add_row(*row)

    console.print(table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    args = parser.parse_args()
    if args.file is not None:
        # File should be generated with tools/coverage/merge_runs.py
        rows = grab_csv_data(args.file)
        rich_print(rows)
    else:
        print("No file specified")


if __name__ == "__main__":
    main()

