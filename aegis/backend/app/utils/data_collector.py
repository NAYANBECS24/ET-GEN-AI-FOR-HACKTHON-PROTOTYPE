from __future__ import annotations

import requests


def fetch_pypi_package(name: str) -> dict:
    r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=5)
    if r.status_code != 200:
        return {}
    return r.json()


def fetch_npm_package(name: str) -> dict:
    r = requests.get(f"https://registry.npmjs.org/{name}", timeout=5)
    if r.status_code != 200:
        return {}
    return r.json()
