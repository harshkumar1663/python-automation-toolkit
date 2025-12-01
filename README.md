# Python Automation Toolkit

Author: Harsh Kumar

A small but production-style toolkit of automation scripts written in Python:

- **File Organizer** – Organize files into subfolders based on extension.
- **Log Analyzer** – Quickly inspect log files for ERROR / WARNING / INFO counts.
- **CSV Cleaner** – Clean messy CSVs (strip whitespace, drop empty rows, fill missing values).

The project is structured as a reusable Python package with a simple CLI entrypoint.

---

## Tech Stack

- Python 3.11+
- Standard Library (`pathlib`, `logging`, `argparse`, `shutil`)
- pandas (for CSV cleaning)
- pytest (for tests)

---

## Installation

```bash
git clone https://github.com/<your-username>/python-automation-toolkit.git
cd python-automation-toolkit

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -e .             # if you keep a pyproject.toml with package info
