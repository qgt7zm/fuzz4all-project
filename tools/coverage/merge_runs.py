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

        # Get model
        with open(os.path.join(run, "model.txt")) as f:
            model_full_name = f.read().strip()
            result["model"] = model_full_name.split("/")[-1]

        # Get final coverage
        with open(os.path.join(run, "coverage.csv")) as f:
            final_trial = f.readlines()[-1].split(",")
            result["line_coverage"] = final_trial[1]
            result["function_coverage"] = final_trial[2]

        # Count total programs
        programs = 0
        for file in os.listdir(run):
            if file.endswith(".fuzz"):
                programs += 1
        result["programs"] = programs

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
            columns = ["target", "language", "model", "line_coverage", "function_coverage", "programs", "valid"]
            writer = csv.DictWriter(csv_file, columns)

            writer.writeheader()
            for result in results:
                writer.writerow(result)
    else:
        print("Not a valid directory")


if __name__ == "__main__":
    main()
