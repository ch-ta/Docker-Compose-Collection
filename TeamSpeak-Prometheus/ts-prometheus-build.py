import subprocess
import os
import sys

def run_command(command, cwd=None):
    """
    Runs a shell command and checks for errors.
    """
    try:
        # Use subprocess.run for simple command execution, capture output if needed
        subprocess.run(command, cwd=cwd, check=True, stdout=sys.stdout, stderr=sys.stderr, text=True)
        print(f"Successfully ran command: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        print(e.stderr)
        sys.exit(1) # Exit the script if a command fails

def automate_docker_workflow(build_dir, compose_dir, image_name, dockerfile_name='Dockerfile'):
    """
    Automates the Docker build and compose up process.
    """
    print(f"--- Starting Docker workflow ---")

    # 0. Take down the Docker container
    print(f"\n--- Running Docker Compose in: {compose_dir} ---")
    compose_down = ["docker", "compose", "down"]
    run_command(compose_down, cwd=compose_dir)

    # 1. CD to the build directory and build the Docker image
    print(f"\n--- Building Docker image in: {build_dir} ---")
    # The command is passed as a list of arguments, which is safer
    build_command = ["docker", "build", "-t", image_name, "-f", dockerfile_name, "."]
    run_command(build_command, cwd=build_dir)

    # 2. CD to the compose directory and run docker-compose up -d
    print(f"\n--- Running Docker Compose in: {compose_dir} ---")
    compose_command = ["docker", "compose", "up", "-d", "--force-recreate"]
    run_command(compose_command, cwd=compose_dir)

    # 3. Clean up the image after starting the container.
    print(f"\n--- Running Docker system prune ---")
    prune_command = ["docker", "system", "prune", "-a", "-f"]
    run_command(prune_command)

    print(f"\n--- Docker workflow completed successfully ---")

if __name__ == "__main__":
    # Define your directories and image name
    # Use absolute paths for robustness
    BUILD_DIR = "${HOME}/teamspeak-prometheus"
    COMPOSE_DIR = "${HOME}/docker/TeamSpeak-Prometheus"
    IMAGE_NAME = "teamspeak-prometheus:latest"
    DOCKERFILE_NAME = "Dockerfile" # Name of your Dockerfile within the build directory

    # Expand environment variables to absolute paths
    BUILD_DIR = os.path.expandvars(BUILD_DIR)
    COMPOSE_DIR = os.path.expandvars(COMPOSE_DIR)

    # Verify directories exist
    if not os.path.isdir(BUILD_DIR):
        print(f"Error: Build directory not found at {BUILD_DIR}")
        sys.exit(1)
    if not os.path.isdir(COMPOSE_DIR):
        print(f"Error: Compose directory not found at {COMPOSE_DIR}")
        sys.exit(1)

    # Run the automation function
    automate_docker_workflow(BUILD_DIR, COMPOSE_DIR, IMAGE_NAME, DOCKERFILE_NAME)
