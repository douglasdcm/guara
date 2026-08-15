# Command Line (CLI) – Quick Reference
## Replay

Previously recorded executions can be replayed using the Guará CLI.

```bash
PYTHONPATH=$(pwd) guara replay -f execution.json
```

A specific execution can be selected:

```bash
PYTHONPATH=$(pwd) guara replay -f execution.json -i <execution-id>
```

## Resume

A replay can resume from a specific transaction or execution identifier.

```bash
PYTHONPATH=$(pwd) guara replay \
    -f execution.json \
    -i <execution-id> \
    --resume
```

This is useful when previous transactions have already completed and should not be executed again.

## Driver Injection

A driver can be supplied when replaying an execution.

```bash
PYTHONPATH=$(pwd) guara replay \
    -f execution.json \
    -d drivers:create_driver
```

The driver is provided at runtime rather than stored in the execution history.

The format is:

```text
module.path:attribute
```

For example:

```text
drivers:create_driver
```

The attribute can represent a driver class or factory.

## CLI

The main CLI command is:

```bash
guara --help
```

Available commands:

```text
guara replay
```

Replay options:

```text
-f, --file       JSON transaction log to replay
-i, --id         Transaction identifier or execution hash
-r, --resume     Resume from the selected execution
-d, --driver     Python path to driver class or factory
```

Example:

```bash
PYTHONPATH=$(pwd) guara replay \
    --file execution.json \
    --id 8f4c2a \
    --resume \
    --driver drivers:create_driver
```
