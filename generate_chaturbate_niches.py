import os
import random
import itertools

WM = "T2CSW"          # ← YOUR NEW AFFILIATE CODE
MAX_PAGES = 2000      # Start with 2000 (safe & fast). Change to 5000 or 10000 later if you want

TAGS = ["bbw", "milf", "petite", "hentai", "teen", "asian", "ebony", "latina", "mature", "squirt", "anal", "bigboobs", "bigass", "feet", "lovense", "18", "young", "curvy", "skinny", "hairy", "shaved", "redhead", "blonde", "goth", "lesbian", "c2c", "cum", "deepthroat", "fuckmachine"]

GENDERS = {"f": "Female", "m": "Male", "t": "Trans", "c": "Couple"}
REGIONS = [None, "asia", "europe_russia", "northamerica", "southamerica"]

niches = []

# Single tag pages
for tag in TAGS:
    for gcode, gname in GENDERS.items():
        for reg in REGIONS:
            slug = f"{tag}-{gcode}"
            if reg: slug += f"-{reg}"
            title = f"Live {tag.upper()} {gname} Cams {' ' + reg.upper() if reg else ''} • Free HD"
            niches.append({
                "slug": slug,
                "title": title,
                "h1": f"🔴 LIVE {tag.upper()} {gname} CHATURBATE",
                "subtitle": f"Real-time {tag} {gname.lower()} cams • Updated every 90 seconds • 18+",
                "filters": {"gender": gcode, "tags": [tag], "region": reg}
            })
            if len(niches) >= MAX_PAGES: break
        if len(niches) >= MAX_PAGES: break
    if len(niches) >= MAX_PAGES: break

# Double tag combos (more pages)
for combo in itertools.combinations(TAGS, 2):
    for reg in REGIONS:
        slug = f"{combo[0]}-{combo[1]}-f"
        if reg: slug += f"-{reg}"
        title = f"Live {combo[0].upper()} + {combo[1].upper()} Cams {' ' + reg.upper() if reg else ''}"
        niches.append({
            "slug": slug,
            "title": title,
            "h1": f"🔴 LIVE {combo[0].upper()} + {combo[1].upper()} CHATURBATE",
            "subtitle": "HD free embeds • Geo-targeted live rooms",
            "filters": {"gender": "f", "tags": list(combo), "region": reg}
        })
        if len(niches) >= MAX_PAGES: break
    if len(niches) >= MAX_PAGES: break

print(f"✅ Generated {len(niches)} niche pages")

# === CREATE FOLDER & FILES ===
base_dir = "."
os.makedirs("niches", exist_ok=True)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="Watch live {title.lower()}. Free HD Chaturbate embeds. Real-time & geo-targeted.">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>body {{ background: #111; color: #fff; }} .card {{ transition: all 0.3s; }} .card:hover {{ transform: scale(1.05); }}</style>
</head>
<body class="min-h-screen p-4">
  <div class="max-w-7xl mx-auto">
    <a href="/index.html" class="text-pink-400 hover:underline">← All 2000+ Niches</a>
    <h1 class="text-4xl font-bold text-center my-6">{h1}</h1>
    <p class="text-center text-pink-400 mb-8">{subtitle}</p>
    
    <div id="grid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"></div>
  </div>

  <div id="modal" class="hidden fixed inset-0 bg-black/90 flex items-center justify-center z-50">
    <div class="w-full max-w-4xl p-4">
      <button onclick="closeModal()" class="absolute top-4 right-4 text-white text-3xl">✕</button>
      <div id="iframe-container"></div>
    </div>
  </div>

  <!-- INTERNAL SEO LINKS -->
  <div class="max-w-7xl mx-auto mt-12 border-t border-zinc-800 pt-8">
    <h2 class="text-2xl font-bold mb-6 text-center">Explore More Niches</h2>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
      {related_links}
    </div>
  </div>

  <script>
    const WM = "{WM}";
    const API = `https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=${{WM}}&client_ip=request_ip&format=json&limit=50&gender={gender}{tags}{region}&hd=true`;

    async function loadRooms() {{
      const res = await fetch(API);
      const data = await res.json();
      const grid = document.getElementById("grid");
      grid.innerHTML = "";

      data.results.sort((a,b) => b.num_users - a.num_users);

      data.results.forEach(room => {{
        const card = document.createElement("div");
        card.className = "card bg-zinc-900 rounded-xl overflow-hidden cursor-pointer";
        card.innerHTML = `
          <img src="${{room.image_url_360x270}}" class="w-full h-48 object-cover">
          <div class="p-3">
            <div class="flex justify-between items-start">
              <div>
                <div class="font-bold text-lg">${{room.username}}</div>
                <div class="text-xs text-pink-400 line-clamp-2">${{room.room_subject}}</div>
              </div>
              <div class="text-right">
                <div class="text-emerald-400 text-sm">${{room.num_users}} now</div>
                <div class="text-xs text-gray-400">${{room.age || ''}} • ${{room.location || 'Unknown'}}</div>
              </div>
            </div>
            <button onclick="openRoom('${{room.iframe_embed_revshare}}')" 
                    class="mt-3 w-full bg-pink-600 hover:bg-pink-500 py-2 rounded-lg font-bold">
              WATCH LIVE FREE
            </button>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function openRoom(html) {{ 
      document.getElementById("iframe-container").innerHTML = html; 
      document.getElementById("modal").classList.remove("hidden"); 
    }}
    function closeModal() {{ 
      document.getElementById("modal").classList.add("hidden"); 
      document.getElementById("iframe-container").innerHTML = ""; 
    }}

    loadRooms();
    setInterval(loadRooms, 90000);
  </script>
</body>
</html>"""

# Generate pages + sitemap + main index
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
main_links = []

for i, niche in enumerate(niches):
    slug = niche["slug"]
    folder = f"niches/{slug}"
    os.makedirs(folder, exist_ok=True)
    
    related = random.sample([n for n in niches if n != niche][:30], min(20, len(niches)-1))
    related_html = "".join(f'<a href="/niches/{r["slug"]}/" class="block bg-zinc-900 p-3 rounded hover:bg-pink-900">{r["title"]}</a>' for r in related)
    
    f = niche["filters"]
    tag_str = "".join(f"&tag={t}" for t in f["tags"])
    reg_str = f"&region={f['region']}" if f["region"] else ""
    
    page_html = html_template.format(
        title=niche["title"],
        h1=niche["h1"],
        subtitle=niche["subtitle"],
        WM=WM,
        gender=f["gender"],
        tags=tag_str,
        region=reg_str,
        related_links=related_html
    )
    
    with open(f"{folder}/index.html", "w", encoding="utf-8") as file:
        file.write(page_html)
    
    url = f"https://YOUR-USERNAME.github.io/niches/{slug}/"   # ← you will replace this later
    sitemap.append(f'  <url><loc>{url}</loc><changefreq>hourly</changefreq><priority>0.8</priority></url>')
    main_links.append(f'<a href="/niches/{slug}/" class="block p-4 bg-zinc-900 hover:bg-pink-900 rounded-xl text-lg">{niche["title"]}</a>')
    
    if (i+1) % 500 == 0:
        print(f"Generated {i+1}/{len(niches)} pages...")

with open("sitemap.xml", "w") as f:
    f.write("\n".join(sitemap))

with open("index.html", "w") as f:
    f.write(f"""<!DOCTYPE html>
<html><head><title>Free Live Chaturbate • {len(niches)} Niches</title>
<style>body{{background:#111;color:#fff;padding:40px;font-family:Arial}}</style>
</head><body>
<h1>🔴 {len(niches)}+ Live Chaturbate Niches (Auto-Generated)</h1>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:15px;margin-top:30px">
{''.join(main_links)}
</div></body></html>""")

print("🎉 ALL DONE! Your 2000+ pages are ready in the 'niches' folder.")
