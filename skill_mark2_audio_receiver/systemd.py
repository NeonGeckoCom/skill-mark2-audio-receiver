import subprocess


# TODO: Logging
def normalize_service_name(service_name: str) -> str:
    return f"{service_name}.service" if not service_name.endswith(".service") else service_name


def interact_with_service(service_name: str, command: str) -> bool:
    subprocess.run(["sudo", "systemctl", command, normalize_service_name(service_name)], check=True)
    return True


def get_service_status(service_name: str):
    result = subprocess.run(
        ["systemctl", "status", normalize_service_name(service_name)], stdout=subprocess.PIPE, check=True
    )
    return result.stdout.decode("utf-8")


def reload_daemon():
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    return True
