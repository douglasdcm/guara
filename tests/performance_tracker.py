"""
The module needed for reading the performance metrics
needed.
"""
import psutil
import time
import threading
import subprocess


def monitor_resources(interval=1):
    """
    Monitor and print CPU, RAM, and Disk usage at regular intervals.
    :param interval: Time in seconds between measurements
    """
    try:
        print("Monitoring system resources... (Press Ctrl+C to stop)")
        print(f"{'Time':<10}{'CPU (%)':<10}{'RAM (%)':<10}{'Disk (%)':<10}")
        start_time = time.time()

        while True:
            cpu_usage = psutil.cpu_percent(interval=None)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            elapsed_time = time.time() - start_time

            print(f"{elapsed_time:<10.2f}{cpu_usage:<10.2f}{ram_usage:<10.2f}{disk_usage:<10.2f}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

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
    monitoring_interval = 1  # Set the monitoring interval in seconds

    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_resources, args=(monitoring_interval,), daemon=True)
    monitor_thread.start()

    # Run the test script
    run_test_script(test_script)

    # Wait for the monitoring thread to finish (optional)
    monitor_thread.join()
