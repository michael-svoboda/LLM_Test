import subprocess
import time

def give_run_permission(working_directory, bash_command):
    full_command = f"chmod +x ./{bash_command}"
    result = subprocess.run(full_command,
                            cwd=working_directory,
                            shell=True,
                            capture_output=True,
                            text=True)
    print(result)

def start_screen_session(working_directory, custom_name, bash_command):
    give_run_permission(working_directory, bash_command)
    print("session name:", custom_name)
    print("session bash command:", bash_command)

    kill_screen_session(custom_name)
    time.sleep(5)
    print(f"starting screen session : {custom_name}")
    full_command = f"screen -dmS {custom_name}  bash -c './{bash_command}'"

    print("start screen command:")
    print(full_command)
    result = subprocess.run(full_command,
                            cwd=working_directory,
                            shell=True,
                            capture_output=True,
                            text=True)
    print(result)

def kill_screen_session(custom_name):
    try:
        result = subprocess.run(f"screen -S {custom_name} -X quit",
                                shell=True,
                                capture_output=True,
                                text=True)

        print("kill screen result:")
        print(result)

        if result.returncode == 0:
            print(f"Successfully killed screen session: {custom_name}")
        else:
            print(f"Failed to kill screen session: {custom_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

