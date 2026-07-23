# import math


# def compute_node_positions(count, radius=190, cx=400, cy=300):
#     positions = []
#     for i in range(count):
#         angle = (2 * math.pi * i / count) - math.pi / 2
#         x = cx + radius * math.cos(angle)
#         y = cy + radius * math.sin(angle)
#         positions.append((round(x, 1), round(y, 1)))
#     return positions


# def build_architecture_svg(nodes, width=800, height=620):
#     cx, cy = width / 2, height / 2
#     radius = min(width, height) / 2 - 100
#     positions = compute_node_positions(len(nodes), radius=radius, cx=cx, cy=cy)

#     svg = f'<svg class="arch-svg" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'

#     # connection lines
#     for node, (x, y) in zip(nodes, positions):
#         svg += f'<line id="arch-line-{node["id"]}" class="arch-line" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}"></line>'

#     # invisible motion paths + traveling data packets
#     for i, (node, (x, y)) in enumerate(zip(nodes, positions)):
#         path_id = f"arch-path-{node['id']}"
#         svg += f'<path id="{path_id}" d="M {cx},{cy} L {x},{y}" fill="none" stroke="none"></path>'
#         svg += f'''
#         <circle class="arch-packet" r="4">
#             <animateMotion dur="{2.4 + (i % 4) * 0.3}s" repeatCount="indefinite" begin="{i * 0.25}s">
#                 <mpath href="#{path_id}"></mpath>
#             </animateMotion>
#         </circle>
#         '''

#     # surrounding nodes (with inner float wrapper, staggered delay)
#     for i, (node, (x, y)) in enumerate(zip(nodes, positions)):
#         delay = round(i * 0.35, 2)
#         svg += f'''
#         <g class="arch-node" data-id="{node["id"]}" data-name="{node["name"]}" data-desc="{node["desc"]}"
#            transform="translate({x},{y})">
#             <g class="arch-node-float" style="animation-delay:{delay}s;">
#                 <circle class="arch-node-glow" r="34"></circle>
#                 <circle class="arch-node-dot" r="26"></circle>
#                 <foreignObject x="-13" y="-13" width="26" height="26" style="pointer-events:none;">
#                     <div xmlns="http://www.w3.org/1999/xhtml" class="arch-icon-wrap">
#                         <i class="{node["icon"]}"></i>
#                     </div>
#                 </foreignObject>
#                 <text class="arch-node-label" x="0" y="48" text-anchor="middle">{node["name"]}</text>
#             </g>
#         </g>
#         '''

#     # center node (drawn last = on top)
#     svg += f'''
#     <g id="arch-center" class="arch-center-node" transform="translate({cx},{cy})">
#         <circle class="arch-node-glow center-glow" r="62"></circle>
#         <circle class="arch-node-dot center-dot" r="44"></circle>
#         <image href="/static/dworker-icon-mono.png" x="-28" y="-28" width="56" height="56"></image>
#         <text class="arch-center-sublabel" x="0" y="72" text-anchor="middle">D-Worker</text>
#     </g>
#     '''

#     svg += '</svg>'
#     return svg, positions, cx, cy


# def build_architecture_data(nodes, positions):
#     return [
#         {"id": n["id"], "name": n["name"], "desc": n["desc"], "x": x, "y": y}
#         for n, (x, y) in zip(nodes, positions)
#     ]

import math


def compute_node_positions(count, radius=190, cx=400, cy=300):
    positions = []
    for i in range(count):
        angle = (2 * math.pi * i / count) - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        positions.append((round(x, 1), round(y, 1)))
    return positions


def build_architecture_svg(nodes, width=800, height=620):
    cx, cy = width / 2, height / 2
    radius = min(width, height) / 2 - 100
    positions = compute_node_positions(len(nodes), radius=radius, cx=cx, cy=cy)

    svg = f'<svg class="arch-svg" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'

    # connection lines
    for node, (x, y) in zip(nodes, positions):
        svg += f'<line id="arch-line-{node["id"]}" class="arch-line" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}"></line>'

    # invisible motion paths + traveling data packets
    for i, (node, (x, y)) in enumerate(zip(nodes, positions)):
        path_id = f"arch-path-{node['id']}"
        svg += f'<path id="{path_id}" d="M {cx},{cy} L {x},{y}" fill="none" stroke="none"></path>'
        svg += f'''
        <circle class="arch-packet" r="4">
            <animateMotion dur="{2.4 + (i % 4) * 0.3}s" repeatCount="indefinite" begin="{i * 0.25}s">
                <mpath href="#{path_id}"></mpath>
            </animateMotion>
        </circle>
        '''

    # surrounding nodes (with inner float wrapper, staggered delay)
    for i, (node, (x, y)) in enumerate(zip(nodes, positions)):
        delay = round(i * 0.35, 2)
        svg += f'''
        <g class="arch-node" data-id="{node["id"]}" data-name="{node["name"]}" data-desc="{node["desc"]}"
           transform="translate({x},{y})">
            <g class="arch-node-float" style="animation-delay:{delay}s;">
                <circle class="arch-node-glow" r="34"></circle>
                <circle class="arch-node-dot" r="26"></circle>
                <foreignObject x="-13" y="-13" width="26" height="26" style="pointer-events:none;">
                    <div xmlns="http://www.w3.org/1999/xhtml" class="arch-icon-wrap">
                        <i class="{node["icon"]}"></i>
                    </div>
                </foreignObject>
                <text class="arch-node-label" x="0" y="48" text-anchor="middle">{node["name"]}</text>
            </g>
        </g>
        '''

    # center node (drawn last = on top)
    svg += f'''
    <g id="arch-center" class="arch-center-node" transform="translate({cx},{cy})">
        <circle class="arch-node-glow center-glow" r="62"></circle>
        <circle class="arch-node-dot center-dot" r="44"></circle>
        <image href="/static/dworker-icon-mono.png" x="-28" y="-28" width="56" height="56"></image>
        <text class="arch-center-sublabel" x="0" y="72" text-anchor="middle">D-Worker</text>
    </g>
    '''

    svg += '</svg>'
    return svg, positions, cx, cy


def build_architecture_data(nodes, positions):
    return [
        {"id": n["id"], "name": n["name"], "desc": n["desc"], "x": x, "y": y}
        for n, (x, y) in zip(nodes, positions)
    ]