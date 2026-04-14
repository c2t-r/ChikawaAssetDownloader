from pathlib import Path

import requests
from catalog import load_catalog_bytes

VERSION = "Prd_2.0.1"
OCTO_SERVER_DOMAIN = "resources-data.jp.chiikawa-pocket.com"
RELEASE_ID_API = f"https://resources-data.jp.chiikawa-pocket.com/tag/{VERSION}"
OUT_PATH = Path("out")


def main() -> None:
    resp = requests.get(RELEASE_ID_API)
    resp.raise_for_status()
    release_id = resp.text

    url = f"https://{OCTO_SERVER_DOMAIN}/{release_id}/a/a/catalog.bin"
    resp = requests.get(url)
    resp.raise_for_status()
    catalog = load_catalog_bytes(resp.content)

    for bundle in catalog.asset_bundle:
        if "http" not in bundle.load_path:
            continue
        url = bundle.load_path.replace("OCTO_SERVER_DOMAIN", OCTO_SERVER_DOMAIN).replace(
            "OCTO_SERVER_RELEASE_ID", release_id
        )
        print(url)

        resp = requests.get(url)
        resp.raise_for_status()

        out = OUT_PATH / "/".join(url.split("/")[-2:])
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "wb") as f:
            f.write(resp.content)


if __name__ == "__main__":
    main()
