# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

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
        while not stop_event.is_set():
            start_time: float = time()
            elapsed_time: float = time() - start_time
            cpu_usage: float = cpu_percent(interval=None)
            ram_usage: float = virtual_memory().percent
            real_disk_usage: float = disk_usage("/").percent
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
        process = run(["python", "tests/performance/script_2_initializer.py"], check=True)
        return process.returncode
    except CalledProcessError as error:
        LOGGER.error(f"Error occurred while running the test script.\nError: {error}")
        return error.returncode


csv_output_directory: str = "./data/"
current_time: str = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_output_file: str = f"{csv_output_directory}/resource_metrics.{current_time}.csv"
monitoring_interval: int = 1
stop_event: Event = Event()
monitor_thread: Thread = Thread(
    target=monitor_resources,
    args=(csv_output_file, stop_event, monitoring_interval),
    daemon=True,
)
monitor_thread.start()
LOGGER.info("Running The Test Script...")
SECONDS = 60 * 5
s = time()
while time() - s < SECONDS:
    exit_code: int = run_test_script()
stop_event.set()
monitor_thread.join()
LOGGER.info(
    f"""Test script finished and the metrics saved.\n
    Exit Code: {exit_code}\n
    Metrics File: {csv_output_file}"""
)
