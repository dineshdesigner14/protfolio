import random

BG_ICONS = [
    "fa-brands fa-docker", "fa-brands fa-aws", "fa-brands fa-python",
    "fa-brands fa-git-alt", "fa-brands fa-github", "fa-brands fa-jenkins",
    "fa-brands fa-linux", "fa-solid fa-server", "fa-solid fa-database",
    "fa-solid fa-network-wired", "fa-solid fa-cloud", "fa-solid fa-infinity",
    "fa-solid fa-diagram-project", "fa-solid fa-microchip",
]

def generate_background_icons(count: int = 24):
    icons = []
    for _ in range(count):
        icons.append({
            "class": random.choice(BG_ICONS),
            "top": f"{random.randint(0, 95)}vh",
            "left": f"{random.randint(0, 95)}vw",
            "size": f"{random.randint(20, 48)}px",
            "duration": f"{random.randint(14, 28)}s",
            "delay": f"{random.uniform(0, 8):.1f}s",
            "opacity": round(random.uniform(0.05, 0.15), 2),
        })
    return icons

def render_background_html(count: int = 24) -> str:
    icons = generate_background_icons(count)
    html = '<div class="bg-layer">'
    html += '<div class="blob blob-1"></div><div class="blob blob-2"></div>'
    for ic in icons:
        html += f'''
        <i class="{ic["class"]} bg-icon"
           style="top:{ic["top"]}; left:{ic["left"]};
                  font-size:{ic["size"]}; opacity:{ic["opacity"]};
                  animation-duration:{ic["duration"]};
                  animation-delay:{ic["delay"]};"></i>
        '''
    html += '</div>'
    return html