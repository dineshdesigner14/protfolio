import json
from nicegui import ui, app
from data.icons import render_background_html
from data.projects import PROJECTS
from data.skills import SKILLS
from data.about import ABOUT
from data.experience import EXPERIENCE
from data.certifications import CERTIFICATIONS
from data.achievements import ACHIEVEMENTS
from data.contact import CONTACT
from data.roadmap import STATIONS
from data.dworker import DWORKER, DWORKER_FEATURES, DWORKER_ROADMAP, HERO_TECH_WORDS
from data.dworker_architecture import ARCH_NODES, BOOT_SEQUENCE
from roadmap_builder import build_roadmap_svg, build_roadmap_data_json
from architecture_builder import build_architecture_svg

# ---------- Head / body assets (shared=True so they apply to all pages) ----------
ui.add_head_html('''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
''', shared=True)
ui.add_head_html('<link rel="stylesheet" href="/static/style.css">', shared=True)
ui.add_head_html('<link rel="stylesheet" href="/static/roadmap.css">', shared=True)
ui.add_head_html('<link rel="stylesheet" href="/static/architecture.css">', shared=True)
ui.add_body_html('<script src="/static/roadmap.js"></script>', shared=True)
ui.add_body_html('<script src="/static/architecture.js"></script>', shared=True)

app_static_dir = "static"


def render_navbar():
    with ui.row().classes('navbar w-full justify-between items-center px-8 py-3'):
        ui.label("DINESH KANNAN").classes('font-bold text-lg tracking-wide')
        with ui.row().classes('gap-6 items-center'):
            for label, target in [
                ("About", "#about"), ("D-Worker", "#dworker"), ("Experience", "#experience"),
                ("Work", "#projects"), ("Skills", "#skills"), ("Journey", "#journey"), ("Contact", "#contact")
            ]:
                ui.link(label, target).classes('nav-link no-underline')
            ui.button("Contact Me", on_click=lambda: ui.navigate.to('#contact')) \
                .classes('rounded-full bg-black text-white px-4 py-1')


def render_hero():
    with ui.column().classes('hero-wrap content-layer w-full'):
        ui.html('<span class="hero-badge">🚀 Building D-Worker</span>')
        ui.label("Dinesh Kannan").classes('hero-title')
        ui.html('<h2 class="hero-title gradient-text" style="font-size:clamp(1.8rem,4vw,2.6rem);margin-top:0.4rem;">'
                'Building Reliable<br>Cloud Infrastructure</h2>')
        ui.label("Cloud Engineer • DevOps Engineer • Platform Engineering Enthusiast") \
            .classes('text-gray-500 mt-3')

        ui.html('<p id="typewriter" class="typing"></p>')
        ui.add_body_html(f'''
        <script>
        const words = {HERO_TECH_WORDS};
        let i = 0, j = 0;
        function typeLoop(){{
            const el = document.getElementById('typewriter');
            if (!el) {{ setTimeout(typeLoop, 200); return; }}
            if (j <= words[i].length) {{
                el.textContent = words[i].slice(0, j++);
                setTimeout(typeLoop, 90);
            }} else {{
                setTimeout(() => {{ j = 0; i = (i+1) % words.length; typeLoop(); }}, 1200);
            }}
        }}
        typeLoop();
        </script>
        ''')

        with ui.row().classes('gap-4 mt-8 flex-wrap justify-center'):
            ui.button("Download Resume", icon="download",
                       on_click=lambda: ui.navigate.to(ABOUT["resume_url"], new_tab=True)) \
                .classes('rounded-full px-6 py-2 bg-black text-white')
            ui.button("Explore My Journey", icon="route",
                       on_click=lambda: ui.navigate.to('#journey')) \
                .classes('rounded-full px-6 py-2').props('outline')
            ui.button("Explore D-Worker", icon="rocket_launch",
                       on_click=lambda: ui.navigate.to('#dworker')) \
                .classes('rounded-full px-6 py-2').props('outline')

        with ui.row().classes('gap-10 mt-12'):
            for stat, label in [("40+", "Deployments Automated"), ("99.98%", "Uptime Delivered"), ("12", "Cloud Platforms")]:
                with ui.column().classes('items-center'):
                    ui.label(stat).classes('text-2xl font-bold gradient-text')
                    ui.label(label).classes('text-xs text-gray-500')


def render_about():
    with ui.column().classes('content-layer w-full items-center py-20 px-6').props('id=about'):
        with ui.row().classes('glass-card max-w-3xl w-full p-8 gap-8 items-start flex-wrap justify-center'):
            ui.image(ABOUT["photo_url"]).classes('w-36 h-36 rounded-full object-cover')
            with ui.column().classes('flex-1 min-w-[260px]'):
                ui.label(ABOUT["greeting"]).classes('text-2xl font-bold mb-3')
                for para in ABOUT["story"]:
                    ui.label(para).classes('text-sm text-gray-600 leading-relaxed mb-3')


def render_dworker_architecture():
    svg_html, positions, cx, cy = build_architecture_svg(ARCH_NODES)

    with ui.column().classes('items-center w-full mt-16'):
        ui.label("Live Architecture").classes('text-2xl font-bold mb-2')
        ui.label("How D-Worker connects the pieces together.").classes('text-gray-500 mb-8')

        with ui.element('div').props('id=dworker-architecture').classes('w-full'):
            ui.html('''
            <div id="arch-boot-overlay" class="arch-boot-overlay">
                <div id="arch-boot-text" class="arch-boot-text"></div>
            </div>
            ''')
            with ui.element('div').props('id=arch-stage'):
                ui.html(svg_html)
                ui.html('<div id="arch-tooltip" class="arch-tooltip"></div>')

    ui.add_body_html(f'<script>window.ARCH_BOOT_SEQUENCE = {json.dumps(BOOT_SEQUENCE)};</script>')


def render_dworker():
    with ui.column().classes('content-layer w-full items-center py-20 px-6').props('id=dworker'):
        with ui.column().classes('glass-card dworker-hero-card max-w-4xl w-full p-10 items-center text-center'):
            ui.image('/static/dworker-logo-stacked.png').classes('w-48 mx-auto mb-3')
            ui.label(DWORKER["tagline"]).classes('text-lg text-sky-700 font-medium mb-4')
            ui.html(f'<span class="status-badge">{DWORKER["status"]}</span>')
            ui.label(DWORKER["description"]).classes('text-sm text-gray-600 leading-relaxed max-w-2xl mt-5')

            with ui.row().classes('gap-3 mt-6 flex-wrap justify-center'):
                ui.button("View Features", on_click=lambda: ui.navigate.to('#dworker-features')).props('outline').classes('rounded-full px-5')
                ui.button("View Roadmap", on_click=lambda: ui.navigate.to('#dworker-roadmap')).props('outline').classes('rounded-full px-5')
                ui.button("GitHub", icon="code",
                           on_click=lambda: ui.navigate.to(DWORKER["github"], new_tab=True)) \
                    .classes('rounded-full px-5 bg-black text-white')

        # Features grid
        with ui.column().classes('items-center w-full mt-16').props('id=dworker-features'):
            ui.label("Features").classes('text-2xl font-bold mb-8')
            with ui.row().classes('flex-wrap gap-5 justify-center max-w-5xl items-stretch'):
                for f in DWORKER_FEATURES:
                    with ui.card().classes('glass-card dworker-feature-card w-40'):
                        ui.html(f'<div class="skill-icon" style="margin:0 auto;"><i class="{f["icon"]}"></i></div>')
                        ui.label(f["name"]).classes('text-sm font-semibold mt-3')

        # Roadmap
        with ui.column().classes('items-center w-full mt-16').props('id=dworker-roadmap'):
            ui.label("Development Roadmap").classes('text-2xl font-bold mb-8')
            with ui.row().classes('flex-wrap gap-6 justify-center max-w-5xl items-stretch'):
                for i, v in enumerate(DWORKER_ROADMAP):
                    with ui.card().classes(f'glass-card roadmap-version-card v{i+1} w-72 p-6'):
                        ui.label(v["version"]).classes('text-lg font-bold')
                        ui.label(v["label"]).classes('text-sky-600 text-sm mb-3')
                        for item in v["items"]:
                            ui.label(f'• {item}').classes('text-sm text-gray-600')

        # Live architecture visualization
        render_dworker_architecture()


def render_experience():
    with ui.column().classes('content-layer w-full items-center py-20 px-6').props('id=experience'):
        ui.label("Experience").classes('text-3xl font-bold mb-10')
        with ui.column().classes('max-w-2xl w-full gap-6'):
            for job in EXPERIENCE:
                with ui.card().classes('glass-card p-6'):
                    with ui.row().classes('justify-between items-center flex-wrap'):
                        ui.label(job["role"]).classes('text-lg font-bold')
                        ui.label(job["period"]).classes('text-xs text-gray-500')
                    ui.label(job["company"]).classes('text-sky-600 text-sm mb-2')
                    for point in job["points"]:
                        ui.label(f'• {point}').classes('text-sm text-gray-600')


def render_projects():
    with ui.column().classes('content-layer w-full items-center py-20 px-6').props('id=projects'):
        ui.label("Selected Work").classes('text-3xl font-bold mb-2')
        ui.label("Production systems built for scale and reliability.").classes('text-gray-500 mb-10')
        with ui.row().classes('flex-wrap gap-6 justify-center max-w-6xl items-stretch'):
            for p in PROJECTS:
                with ui.card().classes('glass-card w-80 p-5'):
                    if p["featured"]:
                        ui.html('<span class="featured-badge">⭐ Featured</span>')
                    ui.label(p["title"]).classes('text-xl font-bold mt-2')
                    ui.label(p["desc"]).classes('text-gray-500 text-sm mt-1')
                    with ui.row().classes('gap-2 flex-wrap mt-3'):
                        for tag in p["tags"]:
                            ui.html(f'<span class="badge-tag">{tag}</span>')
                    with ui.row().classes('gap-3 mt-4'):
                        ui.button("GitHub", icon="code",
                                   on_click=lambda p=p: ui.navigate.to(p["github"], new_tab=True)) \
                            .props('flat')
                        ui.button("Live Demo", icon="open_in_new",
                                   on_click=lambda p=p: ui.navigate.to(p["demo"], new_tab=True)) \
                            .props('flat')


def render_skills():
    with ui.column().classes('content-layer w-full items-center py-20 px-6 bg-sky-50/40').props('id=skills'):
        ui.label("The Arsenal").classes('text-3xl font-bold mb-2')
        ui.label("Tech stack optimized for speed, reliability, and scale.").classes('text-gray-500 mb-10')
        with ui.row().classes('flex-wrap gap-6 justify-center max-w-6xl items-stretch'):
            for s in SKILLS:
                with ui.card().classes('glass-card w-64 p-5'):
                    ui.html(f'<div class="skill-icon"><i class="{s["icon"]}"></i></div>')
                    ui.label(s["category"]).classes('font-bold mt-3')
                    for item in s["items"]:
                        ui.label(f'• {item}').classes('text-sm text-gray-500')


def render_certifications():
    with ui.column().classes('content-layer w-full items-center py-20 px-6').props('id=certifications'):
        ui.label("Certifications").classes('text-3xl font-bold mb-10')
        with ui.row().classes('flex-wrap gap-6 justify-center max-w-5xl items-stretch'):
            for c in CERTIFICATIONS:
                with ui.card().classes('glass-card w-64 p-5 items-center text-center'):
                    ui.html(f'<div class="skill-icon"><i class="{c["icon"]}"></i></div>')
                    ui.label(c["name"]).classes('font-bold text-sm mt-3')
                    ui.label(c["year"]).classes('text-xs text-gray-500')


def render_roadmap():
    svg_html, positions = build_roadmap_svg(STATIONS)
    data_json = build_roadmap_data_json(STATIONS, positions)

    with ui.column().classes('content-layer w-full items-center py-20 px-6 bg-sky-50/40').props('id=journey'):
        ui.label("My Journey").classes('text-3xl font-bold mb-2')
        ui.label("Take the road trip through my career — click any stop.").classes('text-gray-500 mb-10')

        with ui.element('div').classes('roadmap-wrap'):
            ui.html(svg_html)

        ui.html('''
        <div id="roadmap-popup-overlay" class="roadmap-popup-overlay">
            <div class="roadmap-popup" id="roadmap-popup-content"></div>
        </div>
        ''')

        ui.add_body_html(f'<script>window.ROADMAP_STATIONS = {data_json};</script>')


def render_achievements():
    with ui.column().classes('content-layer w-full items-center py-20 px-6').props('id=achievements'):
        ui.label("Achievements").classes('text-3xl font-bold mb-10')
        with ui.row().classes('flex-wrap gap-10 justify-center max-w-5xl'):
            for i, a in enumerate(ACHIEVEMENTS):
                with ui.column().classes('items-center'):
                    ui.html(f'<div class="counter gradient-text" data-target="{a["number"]}" '
                            f'data-suffix="{a["suffix"]}" id="counter-{i}">0</div>')
                    ui.label(a["label"]).classes('text-sm text-gray-500 mt-1')
        ui.add_body_html('''
        <script>
        function animateCounters() {
            document.querySelectorAll('.counter').forEach(el => {
                const target = parseInt(el.dataset.target);
                const suffix = el.dataset.suffix || '';
                let current = 0;
                const step = Math.max(1, Math.ceil(target / 60));
                const interval = setInterval(() => {
                    current += step;
                    if (current >= target) { current = target; clearInterval(interval); }
                    el.textContent = current + suffix;
                }, 25);
            });
        }
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) { animateCounters(); observer.disconnect(); }
            });
        }, { threshold: 0.3 });
        const target = document.querySelector('.counter');
        if (target) observer.observe(target.closest('.content-layer'));
        </script>
        ''')


def render_contact():
    with ui.column().classes('content-layer w-full items-center py-24 px-6').props('id=contact'):
        with ui.row().classes('gap-8 max-w-3xl w-full flex-wrap justify-center items-stretch'):

            with ui.card().classes('glass-card p-10 flex-1 min-w-[280px] items-center text-center') \
                    .style('background: #0b0b0f; color: white;'):
                ui.label("Ready to define the next standard?").classes('text-2xl font-bold')
                ui.label("Currently accepting select freelance projects for Q3 2026.") \
                    .classes('text-gray-300 mt-2 mb-6')

                name = ui.input("Name").classes('w-full').props('dark filled')
                email = ui.input("Email").classes('w-full').props('dark filled')
                message = ui.textarea("Message").classes('w-full').props('dark filled')

                def handle_submit():
                    if not name.value or not email.value:
                        ui.notify("Please fill in name and email", type="warning")
                        return
                    ui.notify("Message sent — thanks for reaching out!", type="positive")
                    name.value = ""
                    email.value = ""
                    message.value = ""

                ui.button("Start a Conversation", on_click=handle_submit) \
                    .classes('submit-btn mt-4 w-full')

            with ui.card().classes('glass-card p-8 flex-1 min-w-[260px] gap-4'):
                ui.label("Or reach me directly").classes('text-lg font-bold mb-2')

                with ui.row().classes('items-center gap-3'):
                    ui.html('<i class="fa-solid fa-envelope contact-icon"></i>')
                    ui.link(CONTACT["email"], f'mailto:{CONTACT["email"]}').classes('text-sm text-gray-700 no-underline')

                with ui.row().classes('items-center gap-3'):
                    ui.html('<i class="fa-brands fa-github contact-icon"></i>')
                    ui.link("GitHub", CONTACT["github"], new_tab=True).classes('text-sm text-gray-700 no-underline')

                with ui.row().classes('items-center gap-3'):
                    ui.html('<i class="fa-brands fa-linkedin contact-icon"></i>')
                    ui.link("LinkedIn", CONTACT["linkedin"], new_tab=True).classes('text-sm text-gray-700 no-underline')

                with ui.row().classes('items-center gap-3'):
                    ui.html('<i class="fa-solid fa-file-arrow-down contact-icon"></i>')
                    ui.link("Download Resume", CONTACT["resume_url"], new_tab=True).classes('text-sm text-gray-700 no-underline')


def render_footer():
    with ui.column().classes('content-layer w-full items-center py-6'):
        ui.image('/static/dworker-logo-horizontal.png').classes('w-40 mb-2')
        ui.html('<div class="footer" style="padding-top:0;">© 2026 Dinesh Kannan · Crafted with NiceGUI</div>')


@ui.page('/')
def main_page():
    ui.html(render_background_html(24))
    render_navbar()
    render_hero()
    render_about()
    render_dworker()
    render_experience()
    render_projects()
    render_skills()
    render_certifications()
    render_roadmap()
    render_achievements()
    render_contact()
    render_footer()


import os
app.add_static_files('/static', app_static_dir)

ui.run(title="Dinesh Kannan — Portfolio", favicon="static/dworker-favicon.png",
       host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

