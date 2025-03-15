# Introduction

This folder stores the performance results of the framework
- `result (folder)`: contains all the results of previous executions
- `app.py`: the user transactions to be tested
- `transactions.py`: the system under testing. A basic To-do list. The SUT does not interact witnany exteral colaborator (servers, REST APIs...)
- `performance-analyzer.ods`: presents the `*.csv` content in a serial graph. To use it, just copy and paste the file content in colums A to E. Check if the graph is using all pasted data
- `script_1.py`: the test scrip. It calls the user transations, collects the metrics like memory, disk... and flush it to `./data/script_1*.csv`
- `script_2_initializer.py`: calls the user transactions before the execution of the `script_2.py`
- `script_2.py`: run the script_2_initialzer.py by subprocesses, collects the host metrics and flush them to `./data/resource_metrics*.csv`

# Running the tests
```
python3.11 -m venv venv
source venv/bin/activate
pip install -r test-requirements.txt
mkdir data
python -m pytest -k test_preformance_async
```