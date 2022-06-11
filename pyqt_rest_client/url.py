from urllib.parse import urljoin
import pyqt_rest_client as client


def url(url_parts: list, args: dict = None) -> str:
    if not url_parts:
        raise ValueError("url_parts: [] are empty")

    if "" in url_parts:
        raise ValueError(f"some parts of url are empty: {url_parts}")

    relative_url = f'{"/".join(url_parts)}/'

    if args:
        args_pairs = [f"{k}={v}" for k, v in args.items() if v]
        relative_url += "?" + "&".join(args_pairs)  # args_path

    return urljoin(client.login_data.base_url, relative_url)
