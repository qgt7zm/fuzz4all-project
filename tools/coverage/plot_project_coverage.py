# Figure 4: Coverage trend of Fuzz4All against state-of-the-art fuzzers (project version)
import matplotlib as mpl
from matplotlib import pyplot as plt

# set plot to use latex fonts

plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pacoty.mplstyle"
)
plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.weight"] = "bold"
plt.rcParams.update({"font.size": 14})

plt.rcParams["axes.facecolor"] = "#f3f7ff"
plt.rcParams["axes.edgecolor"] = "black"
mpl.rcParams["grid.color"] = "#cad4e5"
mpl.rcParams["grid.linewidth"] = 1.2

# dark blue
mpl.rcParams["a xes.edgecolor"] = "#0b2457"
mpl.rcParams["axes.linewidth"] = 1.2

BASE_DIR = "outputs/"


def grab_line_cov(lines, change_time=False, increase_index=True):
    line_cov = []
    func_cov = []
    intervals = []
    time = []
    for index, line in enumerate(lines):
        intervals.append(int(line.split(",")[0]))
        line_cov.append(float(line.split(",")[1]) / 1000)
        # func_cov.append(int(line.split(",")[2]))
        if change_time:
            if increase_index:
                time.append((index + 1) * 24 / len(lines))
            else:
                time.append((index) * 24 / len(lines))
        else:
            time.append(float(line.split(",")[3]) / (60 * 60))

    return line_cov, time, intervals


def extrapolate_points(points, original_time, new_times):
    # linearly extrapolate new points at the new_times
    # based on the points at the original_time
    new_points = []
    for new_time in new_times:
        # find the two points that the new_time is between
        for i in range(len(original_time) - 1):
            if original_time[i] <= new_time < original_time[i + 1]:
                # linearly extrapolate
                new_points.append(
                    points[i]
                    + (points[i + 1] - points[i])
                    * (new_time - original_time[i])
                    / (original_time[i + 1] - original_time[i])
                )
                break

    while len(new_points) != len(new_times):
        new_points.append(points[-1])

    return new_points


def grab_max_min_average(points):
    # points is a list of lists
    # each list is a list of points

    max_points = []
    min_points = []
    average_points = []
    for i in range(len(points[0])):
        max_points.append(max([point[i] for point in points]))
        min_points.append(min([point[i] for point in points]))
        average_points.append(sum([point[i] for point in points]) / len(points))

    return max_points, min_points, average_points


def plot_project_run(language, target, folders):
    print(f"Plotting {language} project coverage run ...")
    # figure size
    plt.figure(figsize=(6, 4))

    new_time = [i for i in range(1, 25)]
    # insert 0.5 at the beginning
    new_time.insert(0, 0.5)

    points = []
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()
        # add zero, zero at the beginning of lines
        lines.insert(0, "0,0,0,0\n")
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)

        # increment of half an hour up to 24 hours
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="starcoder",  # TODO read model name + size
        linewidth=2,
        marker="*",
        markersize=8,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="blue")

    plt.xlabel("Hours")
    plt.ylabel("Coverage (#K lines)")
    # plt.title(title)
    plt.tight_layout()
    # xlimit
    plt.xlim(0, 24)  # TODO fix time axis
    # x ticks every 2 hours
    plt.xticks([i * 2 for i in range(13)])
    plt.legend(loc="lower right")
    plt.savefig(f"fig/coverage-{target}-project.pdf")


if __name__ == "__main__":
    # C++
    plot_project_run(
        "CPP",
        "g++",
        [
            f"{BASE_DIR}cpp_demo1",
            f"{BASE_DIR}cpp_demo2",
        ]
    )

    # C
    plot_project_run(
        "C",
        "gcc",
        [
            f"{BASE_DIR}c_demo1",
            f"{BASE_DIR}c_demo2",
        ]
    )
