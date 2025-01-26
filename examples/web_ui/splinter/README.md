## Compatibility Information

### Selene Integration

The Selene library (v1.0.2) currently has specific compatibility requirements:

- **Supported Python Versions:** 2.7, 3.5, 3.6, 3.7
- **Supported Selenium Versions:** <4.0.0

### Known Issues

Using Selene with Python 3.11 or Selenium >=4.0.0 will result in compatibility errors, such as the `ModuleNotFoundError` for `html5` components in Selenium.  

#### Workaround

If you need to use Selene for testing, consider the following steps:
1. Downgrade to a supported Python version (e.g., Python 3.7).
2. Install a compatible Selenium version (e.g., Selenium 3.141.0).

```bash
python3.7 -m venv selene-env
source selene-env/bin/activate
pip install selene==1.0.2
pip install selenium==3.141.0
