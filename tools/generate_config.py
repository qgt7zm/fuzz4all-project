import argparse
import os

import yaml

# TODO
# Substitute base fields into template
# Take output folder
# Take model name
# Create config


def load_config_file(filepath):
    with open(filepath, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def save_config_file(filepath, config):
    with open(filepath, "w") as f:
        yaml.dump(config, f, Dumper=yaml.Dumper)


def replace_value(dest_cfg, src_cfg, key1, key2):
    dest_cfg[key1][key2] = src_cfg[key1][key2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", type=str, required=True)
    parser.add_argument("--output-folder", type=str, required=True)
    parser.add_argument("--iterations", type=int, default=6000)
    parser.add_argument("--time", type=int, default=12)
    parser.add_argument("--model", type=str, default="ollama/starcoder")
    args = parser.parse_args()
    
    if os.path.isfile(args.base_config):
        # Load config files
        template_file = "config/template.yaml"
        base_file = args.base_config
        template = load_config_file(template_file)
        base = load_config_file(base_file)

        # Modify run config
        template["fuzzing"]["output_folder"] = args.output_folder
        template["fuzzing"]["num"] = args.iterations
        template["fuzzing"]["total_time"] = args.time
        template["ollama"]["model_name"] = args.model

        replace_value(template, base, "target", "path_documentation")
        replace_value(template, base, "target", "trigger_to_generate_input")
        replace_value(template, base, "target", "input_hint")
        replace_value(template, base, "ollama", "model_name")

        # Save run config
        output_file = template_file.split("/")[0] + "/"
        output_file += args.output_folder.split("/")[-1] + ".yaml"
        save_config_file(output_file, template)
    else:
        print("Not a valid config")

