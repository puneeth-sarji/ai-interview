import docker
import tempfile
import os

client = docker.from_env()

def execute_code(code: str, language: str) -> str:
    """
    Executes the provided code securely in a Docker container.
    """
    config = {
        "python": {
            "image": "python:3.11-alpine",
            "cmd": ["python", "/app/code.py"],
            "filename": "code.py"
        },
        "javascript": {
            "image": "node:18-alpine",
            "cmd": ["node", "/app/code.js"],
            "filename": "code.js"
        }
    }

    if language not in config:
        return f"Error: Unsupported language '{language}'"

    lang_config = config[language]
    
    # Write code to a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, lang_config["filename"])
        with open(file_path, "w") as f:
            f.write(code)

        try:
            # Run container and mount the temp directory
            container = client.containers.run(
                image=lang_config["image"],
                command=lang_config["cmd"],
                volumes={temp_dir: {'bind': '/app', 'mode': 'ro'}},
                working_dir="/app",
                detach=True,
                mem_limit="128m", # Restrict memory
                network_disabled=True, # Prevent network access for security
            )
            
            # Wait for execution to finish with a timeout
            result = container.wait(timeout=10) # 10 seconds timeout
            
            logs = container.logs().decode("utf-8")
            container.remove()
            
            if result['StatusCode'] != 0:
                return f"Execution Error:\n{logs}"
            return logs
            
        except docker.errors.ContainerError as e:
            return f"Container Error: {e.stderr.decode('utf-8') if e.stderr else str(e)}"
        except Exception as e:
            return f"Error during execution: {str(e)}"
