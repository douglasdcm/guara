#! bash
set -x
rm -rf mutation.sqlite
cosmic-ray init mutation.toml mutation.sqlite
cosmic-ray --verbosity=INFO baseline mutation.toml
cr-report mutation.sqlite --show-pending
cosmic-ray exec mutation.toml mutation.sqlite
cr-html mutation.sqlite > report.html
