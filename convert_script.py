import pathlib
import yaml
import shutil

def convert_env_to_flat_yaml():
    # Set up paths
    root_dir = pathlib.Path(__file__).parent
    env_files_dir = root_dir / "ENV_FILES"
    output_dir = root_dir / "ConvertedYaml"

    # Clear and recreate output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    print(f"\nStarting conversion from {env_files_dir} to {output_dir}")
    
    # Process each .env file
    for env_file in env_files_dir.glob("*.env"):
        try:
            print(f"Processing {env_file.name}...")
            
            # Create ConfigMap structure
            configmap = {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {
                    "name": env_file.stem.lower().replace('_', '-'),
                    "namespace": "application"
                },
                "data": {}
            }

            # Read and parse .env file
            with env_file.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(('#', 'export ')):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                                value = value[1:-1]
                            configmap["data"][key] = value or ""

            # Write YAML file
            yaml_file = output_dir / f"{env_file.stem}.yaml"
            with yaml_file.open('w', encoding='utf-8') as yf:
                yaml.dump(configmap, yf, default_flow_style=False, sort_keys=False)
            
            print(f"Created: {yaml_file.name}")

        except Exception as e:
            print(f"Error processing {env_file.name}: {str(e)}")
            continue

    print("\nConversion complete!")

if __name__ == "__main__":
    convert_env_to_flat_yaml()