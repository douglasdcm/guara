## Compatibility Information

### Selene Integration

The Selene library (v1.0.2) is **not supported** in environments running Guara with Python 3.11+ due to version incompatibilities.

- **Supported Python Versions:** 2.7, 3.5, 3.6, 3.7
- **Guara Supported Python Versions:** 3.11+
- **Supported Selenium Versions:** <4.0.0

### Known Issues

Using Selene with Python 3.11 or Selenium >=4.12.0 will result in compatibility errors, such as the `ModuleNotFoundError` for `html5` components in Selenium.  

#### Note to Testers

Selene cannot be used in projects running Guara unless Guara is adapted to support older Python versions (2.7 to 3.7). 

This limitation is under discussion. Updates will be provided in future releases.

```bash
python3.7 -m venv selene-env
source selene-env/bin/activate
pip install selene==1.0.2
pip install selenium==4.0.0

