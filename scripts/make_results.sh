#/bin/bash

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate fuzz4all

OUTPUTS="outputs/project"

# Draw figures
python tools/coverage/plot_project_coverage.py --outputs $OUTPUTS
echo "All figures created"

# Draw table
python tools/coverage/merge_runs.py --outputs $OUTPUTS
python tools/coverage/draw_table_project.py --file "$OUTPUTS/results.csv" > fig/coverage-table-project.txt
echo "Table created"

# Backup results
tar -cf fig/project_outputs.tar $OUTPUTS
echo "Results saved to fig/"

# Deactivate conda environment
conda deactivate
