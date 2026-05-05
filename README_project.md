# Fuzz4all Project Instructions

## Development Environment

- Make sure [Docker](https://docs.docker.com/get-started/get-docker/) is installed.
- Run [scripts/start\_container.sh](scripts/start_container.sh) to download and launch the Fuzz4All container in the background.
- Run `sudo docker exec -it my_fuzz4all bash` to login to the container's terminal.
- Note that deleting your container will delete all changes you made to the image, so make sure to transfer your files or mount a shared volume.

## Config Generation

- You may want to install [Ollama](https://ollama.com/) on your host machine since the container does hot have Ollama or the latest repository changes installed.
- If you are running Fuzz4all locally, make sure to create a [conda](https://www.anaconda.com/docs/getting-started/miniconda/main) environment.
- Run [scripts/get\_configs.sh](scripts/get_configs.sh) to generate run configurations and scripts. Modify it to change the model and other parameters.

## Fuzzing

- Follow the [developer's instructions](README_artifact.md) to build your fuzzing targets.
- Once you are satisfied with your config, run `scripts/my_script.sh` if you want to view the output. 
- To ensure your process continues in the background even after your terminal is closed, run `nohup scripts/my_script.sh > /dev/null 2&>1 & disown`.
- To stop your background process, run `ps -ef` and `kill my_pid` with the process whose command starts with `python Fuzz4all/fuzz.py`.

## Coverage

- It is recommended you collect coverage in the Docker container since all the executable paths have already been set up.
- Login to the container and navigate to /home/Fuzz4all.
- Activate your conda environment and run `python tools/coverage/my_lang/collect_coverage.py --folder my_folder --interval my_interval`.
- You may also modify and run [scripts/do\_coverage.sh](scripts/do_coverage.sh) after mounting it to the container.

## Results

- Run [scripts/make\_results.sh](scripts/make\_results.sh) to draw the coverage table and plots.
- You can view your saved figures in fig/ and compare them with mine in [results/](results).
