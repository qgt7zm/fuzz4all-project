import argparse
import csv
import os

def process_run(run):
    result = {}
    try:
        # Get target
        with open(os.path.join(run, "target.txt")) as f:
            result["target"] = f.read().strip()

        # Get language
        with open(os.path.join(run, "language.txt")) as f:
            result["language"] = f.read().strip()

        # Get tool (model)
        with open(os.path.join(run, "model.txt")) as f:
            result["model"] = f.read().strip().split("/")[-1]

        # Get final line coverage
        with open(os.path.join(run, "coverage.csv")) as f:
            result["coverage"] = f.readlines()[-1].split(",")[1]

        # Count total programs
        count = 0
        for file in os.listdir(run):
            if file.endswith(".fuzz"):
                count += 1
        result["count"] = count

        # Count valid programs
        with open(os.path.join(run, "valid.txt")) as f:
            result["valid"] = f.readline().strip()

        return result
    except IOError:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", type=str, required=True)
    args = parser.parse_args()

    if os.path.isdir(args.outputs):
        outputs = args.outputs
        results = []

        # Get results
        for file in os.listdir(outputs):
            run = os.path.join(outputs, file)
            if os.path.isdir(run):
                result = process_run(run)
                if result is not None:
                    results.append(result)
        
        # Save results
        with open(os.path.join(outputs, "results.csv"), "w") as csv_file:
            columns = ["target", "language", "model", "coverage", "count", "valid"]
            writer = csv.DictWriter(csv_file, columns)

            writer.writeheader()
            for result in results:
                writer.writerow(result)
    else:
        print("Not a valid directory")


if __name__ == "__main__":
    main()
