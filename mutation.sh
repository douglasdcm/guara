cosmic-ray init tutorial.toml tutorial.sqlite
cosmic-ray --verbosity=INFO baseline tutorial.toml
cr-report tutorial.sqlite --show-pending
cosmic-ray exec tutorial.toml tutorial.sqlite
cr-html tutorial.sqlite > report.html
