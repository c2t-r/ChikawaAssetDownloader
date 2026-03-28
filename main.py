import json
from pathlib import Path

import requests

OCTO_SERVER_DOMAIN = "resources-data.jp.chiikawa-pocket.com"
RELEASE_ID_API = "https://resources-data.jp.chiikawa-pocket.com/tag/Prd_2.0.0"
CATALOG_PATH = "catalog.json"
OUT_PATH = "out"


def main() -> None:
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    resp = requests.get(RELEASE_ID_API)
    resp.raise_for_status()
    release_id = resp.text  # 97fab255-29be-11f1-9800-0a58a9feac03

    for bundle in catalog["asset_bundle"]:
        if "http" not in bundle["load_path"]:
            continue
        url = (
            bundle["load_path"]
            .replace("OCTO_SERVER_DOMAIN", OCTO_SERVER_DOMAIN)
            .replace("OCTO_SERVER_RELEASE_ID", release_id)
        )
        print(url)

        resp = requests.get(url)
        resp.raise_for_status()

        out = OUT_PATH / Path("/".join(url.split("/")[-2:]))
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "wb") as f:
            f.write(resp.content)


if __name__ == "__main__":
    main()
