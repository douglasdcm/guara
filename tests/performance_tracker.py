"""
The module for tracking the performance metrics of the
library.
"""
from logging import getLogger, Logger
from csv import writer
from time import time, sleep
from psutil import cpu_percent, virtual_memory, disk_usage
from typing import Any, NoReturn
from subprocess import run, CalledProcessError
from datetime import datetime
from threading import Thread


LOGGER: Logger = getLogger("guara")

def monitor_resources(csv_file: str, interval: int = 1) -> None:
    """
    Monitoring the perfomance metrics such as CPU, RAM and disk
    usage and writing them into a CSV file for the generation of
    a chart.

    Args:
        csv_file: (str): Path to the CSV file where metrics will be saved
        interval: (int): Time in seconds between measurements

    Returns:
        (None)
    """
    try:
        LOGGER.info("Monitoring System Resources...")
        file = open(csv_file, mode="w", newline="")
        csv_writer = writer(file)
        csv_writer.writerow(["Time (s)", "CPU (%)", "RAM (%)", "Disk (%)"])
        start_time: float = time()
        write_performance_resource(csv_writer, file, start_time, interval)
    except KeyboardInterrupt:
        LOGGER.info("\nMonitoring stopped.")

def write_performance_resource(writer: Any, file: Any, start_time: float, interval: int) -> NoReturn:
    """
    Writing the performance resource into a CSV file.

    Args:
        writer: (Any): The writer object to write the data
        file: (Any): The file object to write the data
        start_time: (float): The start time of the test
        interval: (int): The interval between measurements

    Returns:
        (NoReturn)
    """
    while True:
        elapsed_time: float = time() - start_time
        cpu_usage: float = cpu_percent(interval=None)
        ram_usage: float = virtual_memory().percent
        real_disk_usage: float = disk_usage('/').percent
        writer.writerow([elapsed_time, cpu_usage, ram_usage, real_disk_usage])
        file.flush()
        sleep(interval)

def run_test_script(script_path: str) -> None:
    """
    Running the test script.

    Args:
        script_path: (str): Path to the Python script to be tested.

    Returns:
        (None)
    """
    try:
        run(["python", script_path], check=True)
    except CalledProcessError as error:
        LOGGER.error(f"Error occurred while running the test script.\nError: {error}")

test_script: str = "./examples/linux_desktop/dogtail/test_integration_with_dogtail.py"
data_script_name: str = test_script.split("/")[-1]
csv_output_directory: str = "./data/"
csv_output_file: str = f"{csv_output_directory}/resource_metrics.{data_script_name}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
monitoring_interval: int = 1
monitor_thread: Thread = Thread(
    target=monitor_resources,
    args=(csv_output_file, monitoring_interval),
    daemon=True
)
monitor_thread.start()
run_test_script(test_script)
monitor_thread.join()
