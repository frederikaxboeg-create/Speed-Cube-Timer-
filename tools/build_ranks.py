"""Laver de små rangliste-filer i ranks/ ud fra WCA's offentlige resultater.

Henter kun de tabeller, der skal bruges (ca. 25 MB), fra WCA's eksport-zip via
HTTP range requests, i stedet for hele filen på ~390 MB.

For hvert puslespil gemmes et udsnit af de sorterede bedste tider, så appen kan
regne ud, hvor mange der har en bedre tid end en given tid:
  ranks/world.json    hele verden
  ranks/countries.json  liste over lande
  ranks/c/<ISO2>.json   hvert land
Kør: python3 tools/build_ranks.py
"""
import csv, io, json, os, sys, urllib.request, zipfile
from collections import defaultdict

API = "https://www.worldcubeassociation.org/api/v0/export/public"
EVENTS = ["222", "333", "444", "555", "666", "777", "333oh", "333bf",
          "pyram", "skewb", "minx", "sq1", "clock"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ranks")
UA = {"User-Agent": "cube-timer-ranks-builder"}


class HttpFile:
    """Read-only, seekable file over HTTP range requests (with a block cache)."""
    BLOCK = 8 << 20

    def __init__(self, url):
        self.url, self.pos, self.buf, self.bstart = url, 0, b"", 0
        req = urllib.request.Request(url, method="HEAD", headers=UA)
        self.size = int(urllib.request.urlopen(req).headers["Content-Length"])

    def seekable(self): return True
    def tell(self): return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos

    def read(self, n=-1):
        if n < 0: n = self.size - self.pos
        n = min(n, self.size - self.pos)
        if n <= 0: return b""
        if not (self.bstart <= self.pos and self.pos + n <= self.bstart + len(self.buf)):
            end = min(self.pos + max(n, self.BLOCK), self.size) - 1
            req = urllib.request.Request(self.url, headers={**UA, "Range": f"bytes={self.pos}-{end}"})
            self.buf, self.bstart = urllib.request.urlopen(req).read(), self.pos
        o = self.pos - self.bstart
        r = self.buf[o:o + n]
        self.pos += len(r)
        return r


def rows(z, name):
    with z.open(f"WCA_export_{name}.tsv") as f:
        yield from csv.DictReader(io.TextIOWrapper(f, "utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)


def sample(values):
    """Keep every value for the top 100, then about every 1 % of the rank.
    Returns {"n": count, "i": [index], "v": [value]} with values sorted ascending."""
    values.sort()
    idx, val, i = [], [], 0
    while i < len(values):
        idx.append(i); val.append(values[i])
        i += max(1, i // 100)
    if idx[-1] != len(values) - 1:
        idx.append(len(values) - 1); val.append(values[-1])
    return {"n": len(values), "i": idx, "v": val}


def main():
    meta = json.load(urllib.request.urlopen(urllib.request.Request(API, headers=UA)))
    if not meta["export_version"].startswith("v2."):
        sys.exit(f"Ukendt eksport-version {meta['export_version']}, tjek formatet.")
    url = urllib.request.urlopen(urllib.request.Request(meta["tsv_url"], headers=UA)).geturl()
    z = zipfile.ZipFile(HttpFile(url))

    countries = {r["id"]: (r["iso2"], r["name"]) for r in rows(z, "countries")}
    person_country = {r["wca_id"]: r["country_id"] for r in rows(z, "persons") if r["sub_id"] == "1"}

    world = {e: {"s": [], "a": []} for e in EVENTS}
    local = defaultdict(lambda: {e: {"s": [], "a": []} for e in EVENTS})
    for kind, table in (("s", "ranks_single"), ("a", "ranks_average")):
        for r in rows(z, table):
            e = r["event_id"]
            if e not in world: continue
            v = int(r["best"])
            if v <= 0: continue
            world[e][kind].append(v)
            c = person_country.get(r["person_id"])
            if c in countries and len(countries[c][0]) == 2:
                local[countries[c][0]][e][kind].append(v)

    date = meta["export_date"][:10]
    def pack(d):
        return {e: {k: sample(v) for k, v in d[e].items() if v} for e in EVENTS if d[e]["s"]}

    os.makedirs(os.path.join(OUT, "c"), exist_ok=True)
    def write(path, obj):
        with open(os.path.join(OUT, path), "w") as f: json.dump(obj, f, separators=(",", ":"))
    write("world.json", {"date": date, "events": pack(world)})
    clist = []
    for iso2, d in sorted(local.items()):
        write(f"c/{iso2}.json", {"date": date, "events": pack(d)})
        name = next(n for i, n in countries.values() if i == iso2)
        clist.append([iso2, name, len(d["333"]["s"])])
    clist.sort(key=lambda c: c[1])
    write("countries.json", {"date": date, "countries": clist})
    print(f"WCA-eksport {date}: {sum(len(world[e]['s']) for e in EVENTS)} singles, {len(clist)} lande")


if __name__ == "__main__":
    main()
