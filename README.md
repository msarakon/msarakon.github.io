# msarakon.github.io

## Refresh lunch menus

From the repository root, run:

```sh
python3 skruudaava/fetch_menus.py
```

This fetches the restaurant menus and updates the cached files in `skruudaava/data/`. An internet connection is required. If a restaurant's fetch fails, its existing cached menu is kept; the script exits with an error only if every fetch fails.