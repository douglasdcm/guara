import time
import datetime
import psutil
import logging


from app import App


def run():
    """Runs the test for SECONDS seconds, save the metrics `time`, `latency`, `cpu`,
    `memory` and `disk` in `data.csv` and the logs of the executin in `script_1.log`
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
        filename=f"./data/script_1_{str(datetime.datetime.now())}.log",
        filemode="w",
    )
    logging.getLogger("guara")

    SECONDS = 60 * 5
    s = time.time()
    csv_writer = f"./data/script_1._{str(datetime.datetime.now())}csv"
    with open(csv_writer, mode="w", newline="") as f:
        f.write("time,latency,cpu,mem,disk\n")
        while time.time() - s < SECONDS:
            start = time.time()
            app = App()
            app.run()
            end = time.time()
            f.write(
                ",".join(
                    [
                        str(datetime.datetime.now()),
                        str((end - start) * 10**3),
                        str(psutil.cpu_percent(interval=1)),
                        str(psutil.virtual_memory().percent),
                        str(psutil.disk_usage("/").percent),
                        "\n",
                    ]
                )
            )
            f.flush()


if __name__ == "__main__":
    run()
