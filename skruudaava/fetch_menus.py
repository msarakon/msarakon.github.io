import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


SOURCES = {
    "palmia": "https://www.palmia.fi/ravintola/ravintola-huippu-34/",
    "bierhaus": "https://www.ardenrestaurants.fi/menut/BHkamppi/",
    "kansis": "https://ravintolakansis.fi/lounas/",
    "bruuveri": "https://bruuveri.fi/lounas/",
}


def fetch_menus(output_dir=Path(__file__).parent / "data"):
    output_dir.mkdir(parents=True, exist_ok=True)
    successes = 0
    for restaurant_id, source in SOURCES.items():
        try:
            request = Request(source, headers={"User-Agent": "KamppiLunchMenus/1.0"})
            with urlopen(request, timeout=30) as response:
                html = response.read().decode(response.headers.get_content_charset() or "utf-8")
            if re.search(r"<(?:html|body|div|p|ul)\b", html, re.IGNORECASE) is None:
                raise ValueError("Restaurant did not return HTML")
            payload = {
                "source": source,
                "fetchedAt": datetime.now(timezone.utc).isoformat(),
                "html": html,
            }
            destination = output_dir / f"{restaurant_id}.json"
            temporary = destination.with_suffix(".tmp")
            temporary.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            temporary.replace(destination)
            successes += 1
            print(f"Updated {restaurant_id}")
        except Exception as error:
            print(f"Failed {restaurant_id}; keeping any cached menu: {error}")
    if successes == 0:
        raise RuntimeError("No restaurant menus could be fetched")


if __name__ == "__main__":
    fetch_menus()