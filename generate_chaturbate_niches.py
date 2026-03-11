import os
import random
import itertools

# ---------------- Configuration ----------------
WM = "T2CSW"
MAX_PAGES = 2000

TAGS = [
"bbw","milf","petite","hentai","asian","ebony","latina","mature","squirt",
"anal","bigboobs","bigass","feet","lovense","curvy","skinny","hairy",
"shaved","redhead","blonde","goth","lesbian","c2c","cum","deepthroat","fuckmachine"
]

GENDERS = {"f": "Female", "m": "Male", "t": "Trans", "c": "Couple"}
REGIONS = [None, "asia", "europe_russia", "northamerica", "southamerica"]

# ---------------- Generate niches ----------------
niches = []

for tag in TAGS:
    for gcode, gname in GENDERS.items():
        for reg in REGIONS:
            slug = f"{tag}-{gcode}"
            if reg: slug += f"-{reg}"

            title = f"Live {tag.upper()} {gname} Cams"
            if reg: title += f" {reg.upper()}"

            niches.append({
                "slug": slug,
                "title": title,
                "h1": f"🔴 LIVE {tag.upper()} {gname} CAMS",
                "subtitle": f"Real-time {tag} {gname.lower()} cams • Updated every 90 seconds",
                "filters": {"gender": gcode, "tags": [tag], "region": reg}
            })

            if len(niches) >= MAX_PAGES: break
        if len(niches) >= MAX_PAGES: break
    if len(niches) >= MAX_PAGES: break

for combo in itertools.combinations(TAGS, 2):
    for reg in REGIONS:
        slug = f"{combo[0]}-{combo[1]}-f"
        if reg: slug += f"-{reg}"
        title = f"Live {combo[0].upper()} + {combo[1].upper()} Cams"
        niches.append({
            "slug": slug,
            "title": title,
            "h1": f"🔴 LIVE {combo[0].upper()} + {combo[1].upper()} CAMS",
            "subtitle": "HD live rooms • Updated every 90 seconds",
            "filters": {"gender": "f", "tags": list(combo), "region": reg}
        })
        if len(niches) >= MAX_PAGES: break
    if len(niches) >= MAX_PAGES: break

print(f"✅ Generated {len(niches)} niches")

# ---------------- Build clusters for auto internal linking ----------------
tag_cluster = {}
gender_cluster = {}
region_cluster = {}

for niche in niches:
    f = niche["filters"]
    main_tag = f["tags"][0]
    gender = f["gender"]
    region = f["region"]

    tag_cluster.setdefault(main_tag, []).append(niche)
    gender_cluster.setdefault(gender, []).append(niche)
    if region:
        region_cluster.setdefault(region, []).append(niche)

def get_related(niche, num_links=20):
    f = niche["filters"]
    main_tag = f["tags"][0]
    gender = f["gender"]
    region = f["region"]

    # Start with same tag cluster
    pool = [n for n in tag_cluster[main_tag] if n != niche]

    # If not enough, add same gender cluster
    if len(pool) < num_links:
        pool += [n for n in gender_cluster[gender] if n != niche and n not in pool]

    # If still not enough, add same region cluster
    if region and len(pool) < num_links:
        pool += [n for n in region_cluster.get(region, []) if n != niche and n not in pool]

    # Shuffle and pick top num_links
    random.shuffle(pool)
    return pool[:num_links]

# ---------------- HTML Template ----------------
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Watch {title}. Free live cams updated every 90 seconds.">
<script src="https://cdn.tailwindcss.com"></script>
<style>
body {{ background:#111; color:#fff; }}
.card:hover {{ transform:scale(1.05); transition:.3s; }}
</style>
</head>
<body class="min-h-screen p-4">

<div class="max-w-7xl mx-auto">
<a href="/index.html" class="text-pink-400">← All Niches</a>
<h1 class="text-4xl font-bold text-center my-6">{h1}</h1>
<p class="text-center text-pink-400 mb-8">{subtitle}</p>
<div id="grid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"></div>
</div>

<div class="max-w-7xl mx-auto mt-12 border-t border-zinc-800 pt-8">
<h2 class="text-2xl font-bold mb-6 text-center">Explore More Niches</h2>
<div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">{related_links}</div>
</div>

<script>
const API = `https://chaturbate.com/api/public/affiliates/onlinerooms/?wm={WM}&client_ip=request_ip&format=json&limit=50&gender={gender}{tags}{region}&hd=true`;

async function loadRooms() {{
    const res = await fetch(API);
    const data = await res.json();
    const grid = document.getElementById("grid");
    grid.innerHTML = "";
    data.results.sort((a,b)=>b.num_users-a.num_users);
    data.results.forEach(room => {{
        const card = document.createElement("div");
        card.className="card bg-zinc-900 rounded-xl overflow-hidden cursor-pointer";
        card.innerHTML=`
            <img src="${{room.image_url_360x270}}" class="w-full h-48 object-cover">
            <div class="p-3">
                <div class="font-bold text-lg">${{room.username}}</div>
                <div class="text-xs text-pink-400">${{room.room_subject}}</div>
                <div class="text-emerald-400 text-sm">${{room.num_users}} watching</div>
                <button onclick="openRoom('${{room.iframe_embed_revshare}}')" class="mt-3 w-full bg-pink-600 py-2 rounded">WATCH</button>
            </div>
        `;
        grid.appendChild(card);
    }});
}}

function openRoom(html) {{
    const modal = document.createElement("div");
    modal.innerHTML = html;
    document.body.appendChild(modal);
}}

loadRooms();
setInterval(loadRooms,90000);
</script>
</body>
</html>
"""

# ---------------- Build pages ----------------
os.makedirs("niches", exist_ok=True)
sitemap = []
main_links = []

for niche in niches:
    slug = niche["slug"]
    folder = f"niches/{slug}"
    os.makedirs(folder, exist_ok=True)

    # Related links via clusters
    related = get_related(niche, num_links=20)
    related_html = "".join(
        f'<a href="/niches/{r["slug"]}/" class="block bg-zinc-900 p-3 rounded">{r["title"]}</a>'
        for r in related
    )

    f = niche["filters"]
    tag_str = "".join(f"&tag={t}" for t in f["tags"])
    reg_str = f"&region={f['region']}" if f["region"] else ""

    page = html_template
    page = page.replace("{title}", niche["title"])
    page = page.replace("{h1}", niche["h1"])
    page = page.replace("{subtitle}", niche["subtitle"])
    page = page.replace("{WM}", WM)
    page = page.replace("{gender}", f["gender"])
    page = page.replace("{tags}", tag_str)
    page = page.replace("{region}", reg_str)
    page = page.replace("{related_links}", related_html)

    with open(f"{folder}/index.html","w",encoding="utf-8") as file:
        file.write(page)

    sitemap.append(f"<url><loc>/niches/{slug}/</loc></url>")
    main_links.append(
        f'<a href="/niches/{slug}/" class="block p-4 bg-zinc-900 rounded">{niche["title"]}</a>'
    )

# ---------------- Sitemap ----------------
with open("sitemap.xml","w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    f.write("".join(sitemap))
    f.write("</urlset>")

# ---------------- Homepage ----------------
with open("index.html","w") as f:
    f.write(f"""
<html>
<head>
<title>{len(niches)} Live Cam Niches</title>
<style>
body{{background:#111;color:#fff;font-family:Arial;padding:40px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:15px}}
</style>
</head>
<body>
<h1>{len(niches)} Live Cam Niches</h1>
<div class="grid">{''.join(main_links)}</div>
</body>
</html>
""")

print("🎉 DONE - pages generated:", len(niches))