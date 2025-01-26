"""
The module for tracking the performance metrics of the
library.
"""
from logging import getLogger, Logger
from csv import writer
from time import time, sleep
from psutil import cpu_percent, virtual_memory, disk_usage
from subprocess import run, CalledProcessError
from datetime import datetime
from threading import Thread, Event


LOGGER: Logger = getLogger("guara")

def monitor_resources(csv_file: str, stop_event: Event, interval: int = 1) -> None:
    """
    Monitoring the perfomance metrics such as CPU, RAM and disk
    usage and writing them into a CSV file for the generation of
    a chart.

    Args:
        csv_file: (str): Path to the CSV file where metrics will be saved
        interval: (int): Time in seconds between measurements
        stop_event: (Event): Threading event to signal when to stop monitoring

    Returns:
        (None)
    """
    try:
        LOGGER.info("Monitoring System Resources...")
        file = open(csv_file, mode="w", newline="")
        csv_writer = writer(file)
        csv_writer.writerow(["Time (s)", "CPU (%)", "RAM (%)", "Disk (%)"])
        start_time: float = time()
        while not stop_event.is_set():
            elapsed_time: float = time() - start_time
            cpu_usage: float = cpu_percent(interval=None)
            ram_usage: float = virtual_memory().percent
            real_disk_usage: float = disk_usage('/').percent
            csv_writer.writerow([elapsed_time, cpu_usage, ram_usage, real_disk_usage])
            file.flush()
            sleep(interval)
    except Exception as error:
        LOGGER.error(f"Error during monitoring.\n Error: {error}")

def run_test_script() -> None:
    """
    Running the test script.

    Returns:
        (None)
    """
    try:
        process = run(["python", "-m", "pytest"], check=True)
        return process.returncode
    except CalledProcessError as error:
        LOGGER.error(f"Error occurred while running the test script.\nError: {error}")
        return error.returncode

csv_output_directory: str = "./data/"
csv_output_file: str = f"{csv_output_directory}/resource_metrics.{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
monitoring_interval: int = 1
stop_event: Event = Event()
monitor_thread: Thread = Thread(
    target=monitor_resources,
    args=(csv_output_file, monitoring_interval, stop_event),
    daemon=True
)
monitor_thread.start()
LOGGER.info("Running The Test Script...")
exit_code: int = run_test_script()
stop_event.set()
monitor_thread.join()
LOGGER.info(f"Test script finished and the metrics saved.\n Exit Code: {exit_code}\n Metrics File: {csv_output_file}")
