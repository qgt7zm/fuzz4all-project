import argparse
import os

import yaml


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
    parser.add_argument("--batch-size", type=int, default=30)
    parser.add_argument("--model", type=str, default="ollama/starcoder")
    parser.add_argument("--target", type=str, required=True)
    args = parser.parse_args()
    
    if os.path.isfile(args.base_config):
        # Load config files
        template_cfg = "config/template.yaml"
        base_cfg = args.base_config
        template = load_config_file(template_cfg)
        base = load_config_file(base_cfg)
        output_folder = os.path.normpath(args.output_folder)

        # Modify run config
        template["fuzzing"]["output_folder"] = output_folder
        template["fuzzing"]["num"] = args.iterations
        template["fuzzing"]["total_time"] = args.time
        template["ollama"]["model_name"] = args.model

        replace_value(template, base, "target", "path_documentation")
        replace_value(template, base, "target", "trigger_to_generate_input")
        replace_value(template, base, "target", "input_hint")
        replace_value(template, base, "ollama", "model_name")

        # Save run config
        output_cfg = os.path.dirname(template_cfg)
        output_cfg = os.path.join(output_cfg, os.path.basename(output_folder))
        output_cfg += ".yaml"
        save_config_file(output_cfg, template)
        print("Config generated at", output_cfg)

        # Create run script
        template_script = "scripts/template.sh"
        with open(template_script, "r") as f:
            script = f.read()
            script = script.replace("{CONFIG_FILE}", output_cfg)
            script = script.replace("{OUTPUT_FOLDER}", output_folder)
            script = script.replace("{BATCH_SIZE}", str(args.batch_size))
            script = script.replace("{MODEL_NAME}", args.model)
            script = script.replace("{TARGET}", args.target)
        
        # Save run script
        output_script = os.path.dirname(template_script)
        output_script = os.path.join(output_script, os.path.basename(output_folder))
        output_script += ".sh"
        with open(output_script, "w") as f:
            f.write(script)
        print("Script generated at", output_script)
    else:
        print("Not a valid config")

