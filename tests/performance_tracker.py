"""
The module for tracking the performance metrics of the
library.
"""
import threading
import subprocess
from logging import getLogger, Logger
from csv import writer
from time import time, sleep
from psutil import cpu_percent, virtual_memory, disk_usage


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
        while True:
            elapsed_time: float = time() - start_time
            cpu_usage: float = cpu_percent(interval=None)
            ram_usage: float = virtual_memory().percent
            real_disk_usage: float = disk_usage('/').percent
            csv_writer.writerow([elapsed_time, cpu_usage, ram_usage, real_disk_usage])
            file.flush()
            sleep(interval)
    except KeyboardInterrupt:
        LOGGER.info("\nMonitoring stopped.")

def run_test_script(script_path):
    """
    Run the test script.
    :param script_path: Path to the Python script to be tested
    """
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the test script: {e}")

if __name__ == "__main__":
    test_script = "test_script.py"  # Replace with the path to your test script
    csv_output_file = "resource_metrics.csv"  # CSV file to save metrics
    monitoring_interval = 1  # Set the monitoring interval in seconds

    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_resources, args=(csv_output_file, monitoring_interval), daemon=True)
    monitor_thread.start()

    # Run the test script
    run_test_script(test_script)

    # Wait for the monitoring thread to finish (optional)
    monitor_thread.join()
