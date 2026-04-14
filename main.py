import argparse
from pathlib import Path

import requests
from catalog import load_catalog_bytes

OCTO_SERVER_DOMAIN = "resources-data.jp.chiikawa-pocket.com"
OUT_PATH = Path("out")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chikawa Asset Downloader")
    parser.add_argument("-v", "--v", type=str, required=True, help="Target version (e.g., Prd_2.0.1)")
    args = parser.parse_args()

    version = args.v
    release_id_api = f"https://{OCTO_SERVER_DOMAIN}/tag/{version}"

    resp = requests.get(release_id_api)
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
