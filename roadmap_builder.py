import json


def compute_positions(count, width=1100, height=420, margin=70):
    positions = []
    for i in range(count):
        x = margin + (width - 2 * margin) * (i / (count - 1)) if count > 1 else width / 2
        amplitude = 100
        if i == 0 or i == count - 1:
            amplitude = 40
        y = height / 2 + (amplitude if i % 2 == 0 else -amplitude)
        positions.append((round(x, 1), round(y, 1)))
    return positions


def build_smooth_path(points):
    if not points:
        return ""
    path = f"M {points[0][0]},{points[0][1]} "
    for i in range(1, len(points)):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        cx = round((x0 + x1) / 2, 1)
        path += f"C {cx},{y0} {cx},{y1} {x1},{y1} "
    return path.strip()


def build_roadmap_svg(stations, width=1100, height=420):
    positions = compute_positions(len(stations), width, height)
    path_d = build_smooth_path(positions)

    svg = f'<svg class="roadmap-svg" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<path class="road-base" d="{path_d}" />'
    svg += f'<path id="road-progress" class="road-progress" d="{path_d}" />'
    svg += f'<path class="road-dashes" d="{path_d}" />'

    for i, (station, (x, y)) in enumerate(zip(stations, positions)):
        svg += f'''
        <g class="station" data-id="{station["id"]}" data-index="{i}" data-x="{x}" data-y="{y}"
           transform="translate({x},{y})">
            <circle class="station-glow" r="30"></circle>
            <circle class="station-dot" r="22"></circle>
            <foreignObject x="-14" y="-14" width="28" height="28" style="pointer-events:none;">
                <div xmlns="http://www.w3.org/1999/xhtml" class="station-icon-wrap">
                    <i class="{station["icon"]}"></i>
                </div>
            </foreignObject>
            <text class="station-label" x="0" y="46" text-anchor="middle">{station["name"]}</text>
        </g>
        '''

    start_x, start_y = positions[0]
    svg += f'''
    <g id="bus" class="bus" transform="translate({start_x},{start_y})">
        <ellipse class="bus-shadow" cx="0" cy="26" rx="24" ry="6"></ellipse>
        <rect class="bus-body" x="-22" y="-14" width="44" height="24" rx="8"></rect>
        <rect class="bus-window" x="-16" y="-10" width="32" height="10" rx="3"></rect>
        <circle class="bus-wheel" cx="-12" cy="12" r="6"></circle>
        <circle class="bus-wheel" cx="12" cy="12" r="6"></circle>
    </g>
    '''
    svg += '</svg>'
    return svg, positions


def build_roadmap_data_json(stations, positions):
    data = []
    for station, (x, y) in zip(stations, positions):
        data.append({
            "id": station["id"],
            "name": station["name"],
            "caption": station.get("caption", ""),
            "x": x,
            "y": y,
            "details": station.get("details", {}),
        })
    return json.dumps(data)