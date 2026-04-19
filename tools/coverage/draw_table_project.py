# Table 2: Fuzz4All models comparison (project version)
import argparse
from collections import defaultdict, namedtuple

BASELINE = "starcoder:3b"
FuzzingRun = namedtuple("FuzzingRun", ["programs", "valid", "coverage", "total_lines", "avg_lines"])


def grab_csv_data(csv_file):
    import csv
    import statistics as st

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    # Aggregate rows by target and fuzzing model
    aggregated = defaultdict(lambda: defaultdict(list))
    for row in data:
        target = row["target"]
        fuzzer = row["model"]

        programs = int(row["programs"])
        valid = float(row["valid"])
        valid_percent = valid / programs
        coverage = int(row["line_coverage"])
        total_lines = int(row["lines_of_code"])
        avg_lines = total_lines / programs

        aggregated[target][fuzzer].append(
            FuzzingRun(programs, valid_percent, coverage, total_lines, avg_lines)
        )

    # Average num programs, valid %, coverage, and LoC
    ret_rows = []
    for target, tools in aggregated.items():
        short_target = target.split("/")[-1]
        for tool_name, trials in tools.items():
            avg_programs = int(st.mean([trial.programs for trial in trials]))
            avg_valid = round(st.fmean([trial.valid for trial in trials]), 4)
            avg_coverage = int(st.mean([trial.coverage for trial in trials]))
            avg_total_lines = int(st.mean([trial.total_lines for trial in trials]))
            avg_avg_lines = int(st.mean([trial.avg_lines for trial in trials]))

            ret_rows.append([
                short_target,
                tool_name,
                f"{avg_programs:,}",
                f"{avg_valid:.2%}",
                f"{avg_coverage:,}",
                f"{avg_total_lines:,}",
                f"{avg_avg_lines:,}",
            ])

    # Sort rows by target and model
    # Keep the baseline on top
    ret_rows.sort(key=lambda r: "" if r[1] == BASELINE else r[1])
    ret_rows.sort(key=lambda r: r[0])
    return ret_rows


def rich_print(rows):
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(
        show_header=True,
        header_style="bold magenta",
        title="Fuzz4All fuzzing performance with different models",
    )

    table.add_column("Target", style="dim", no_wrap=True)
    table.add_column("Model", justify="right", style="bold green")
    table.add_column("# Programs", justify="right", style="bold blue")
    table.add_column("% Valid", justify="right", style="bold blue")
    table.add_column("Line Cov.", justify="right", style="bold blue")
    table.add_column("Total LoC", justify="right", style="bold blue")
    table.add_column("Avg. LoC", justify="right", style="bold blue")

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

