"""Generate book illustrations with Pollinations.ai (free, no API key).

Usage: python tools/gen_images.py
Writes PNGs to imagenes/. Seeds are fixed for reproducibility.
"""
import os
import time
import urllib.parse
import urllib.request

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "imagenes")

STYLE = (
    "minimalist flat vector illustration, dark navy blue background, "
    "cyan and warm amber accents, clean geometric shapes, subtle grid, "
    "technical book art, modern editorial style, no text, no letters, no words"
)

# (filename, theme, width, height, seed)
IMAGES = [
    ("cover.png",
     "three glowing paths merging into a single server core, browser window "
     "transforming into backend infrastructure, epic composition", 1200, 1600, 7),
    ("parte-00.png",
     "a browser window dissolving into a server rack, threshold between "
     "frontend and backend worlds", 1200, 500, 10),
    ("parte-01.png",
     "task cards flowing through an API pipeline, endpoints as gates, "
     "checklists and status badges", 1200, 500, 11),
    ("parte-02.png",
     "relational database tables as geometric blueprints, connected by "
     "foreign key lines, postgres elephant silhouette abstracted", 1200, 500, 12),
    ("parte-03.png",
     "shield and key over user identity cards, JWT token as a signed seal, "
     "lock and permission layers", 1200, 500, 13),
    ("parte-04.png",
     "server calling external APIs, network constellation, webhooks as "
     "incoming lightning bolts, parallel paths", 1200, 500, 14),
    ("parte-05.png",
     "fortress wall around an API, log streams flowing, warning signals "
     "contained, observability dashboard shapes", 1200, 500, 15),
    ("parte-06.png",
     "testing pyramid, checkmarks cascading over code, gears verified by "
     "green check marks", 1200, 500, 16),
    ("parte-07.png",
     "shipping containers stacked as application layers, whale-like cargo "
     "ship silhouette, identical boxes", 1200, 500, 17),
    ("parte-08.png",
     "rocket deploying a container to the cloud, CI pipeline arrows, "
     "production globe", 1200, 500, 18),
    ("parte-09.png",
     "collaborative workspace constellation, versioned document branches "
     "like a git tree, team nodes connected realtime", 1200, 500, 19),
]


def generate(filename, theme, w, h, seed):
    prompt = urllib.parse.quote(f"{theme}, {STYLE}")
    url = (
        f"https://image.pollinations.ai/prompt/{prompt}"
        f"?width={w}&height={h}&seed={seed}&nologo=true&model=flux"
    )
    out = os.path.join(BASE_DIR, filename)
    if os.path.exists(out):
        print(f"SKIP {filename}")
        return
    print(f"GEN  {filename} ...", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "book-gen/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(out, "wb") as f:
            f.write(data)
        print(f"OK   {filename} ({len(data)//1024} KB)")
    except Exception as e:
        print(f"FAIL {filename}: {e}")


if __name__ == "__main__":
    os.makedirs(BASE_DIR, exist_ok=True)
    for img in IMAGES:
        generate(*img)
        time.sleep(2)  # be polite to the free API
    print("done")
