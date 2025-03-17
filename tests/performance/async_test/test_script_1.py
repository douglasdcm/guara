# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import time
import datetime
import logging
from pytest import mark
from tests.performance.async_test.app.app import App
import psutil


@mark.skip(reason="Do not run on pipelines. Run it manually on each release")
@mark.asyncio
async def test_performance_async():
    """Runs the test for SECONDS seconds, save the metrics `time`, `latency`, `cpu`,
    `memory` and `disk` in `data.csv` and the logs of the executin in `script_1.log`
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
        filename=f"./data/script_1_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        filemode="w",
    )
    logging.getLogger("guara")

    SECONDS = 60 * 5
    s = time.time()
    csv_writer = f"./data/script_1_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_writer, mode="w", newline="") as f:
        f.write("time,latency,cpu,mem,disk\n")
        while time.time() - s < SECONDS:
            start = time.time()
            app = App()
            await app.run()
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
