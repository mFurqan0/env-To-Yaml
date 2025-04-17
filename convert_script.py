import pathlib
import yaml
import shutil

def convert_env_to_flat_yaml():
    # Root directory = directory where this script resides
    root_dir = pathlib.Path(__file__).parent
    
    # Define input/output directories relative to script location
    env_files_dir = root_dir / "EnvFiles"  # Input .env files
    output_dir = root_dir / "ConvertedYaml"  # Output YAML files

    # Clear existing contents in output directory (if it exists)
    if output_dir.exists():
        for item in output_dir.iterdir():
            if item.is_file():
                item.unlink()  # Delete file
            elif item.is_dir():
                shutil.rmtree(item)  # Delete subdirectory

    # Process each .env file
    for env_file in env_files_dir.glob("*.env"):
        try:
            if not env_file.is_file():
                continue

            # Create a ConfigMap structure
            configmap = {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {
                    "name": env_file.stem.lower().replace('_', '-'),
                    "namespace": "application"
                },
                "data": {}
            }

            # Read the .env file
            with env_file.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(('#', 'export ')):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Handle quoted values
                            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                                value = value[1:-1]
                            configmap["data"][key] = value or ""

            # Write the YAML file
            yaml_file = output_dir / f"{env_file.stem}.yaml"
            with yaml_file.open('w', encoding='utf-8') as yf:
                yaml.dump(
                    configmap,
                    yf,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                    indent=2,
                    width=1000  # Prevent line wrapping
                )
            
            print(f"Converted: {env_file.name} => {yaml_file.name}")

        except Exception as e:
            print(f"Error processing {env_file.name}: {str(e)}")
            continue

if __name__ == "__main__":
    convert_env_to_flat_yaml()