(function () {
    function initRoadmap() {
        const stations = window.ROADMAP_STATIONS;
        if (!stations) { setTimeout(initRoadmap, 200); return; }

        const bus = document.getElementById('bus');
        const progressPath = document.getElementById('road-progress');
        if (!bus || !progressPath) { setTimeout(initRoadmap, 200); return; }

        const totalLength = progressPath.getTotalLength();
        progressPath.style.strokeDasharray = totalLength;
        progressPath.style.strokeDashoffset = totalLength;

        const overlay = document.getElementById('roadmap-popup-overlay');
        const popup = document.getElementById('roadmap-popup-content');

        function updateStationStates(index) {
            document.querySelectorAll('.station').forEach(el => {
                const i = parseInt(el.dataset.index);
                el.classList.remove('completed', 'current', 'future');
                if (i < index) el.classList.add('completed');
                else if (i === index) el.classList.add('current');
                else el.classList.add('future');
            });
        }

        function updateProgress(index) {
            const frac = stations.length > 1 ? index / (stations.length - 1) : 0;
            progressPath.style.strokeDashoffset = totalLength * (1 - frac);
        }

        function moveBusTo(index) {
            const target = stations[index];
            bus.setAttribute('transform', `translate(${target.x},${target.y})`);
            bus.classList.add('moving');
            setTimeout(() => bus.classList.remove('moving'), 1200);
            updateProgress(index);
            updateStationStates(index);
        }

        function buildPopupHtml(station) {
            const d = station.details || {};
            let html = `<button class="popup-close" onclick="window.__closeRoadmapPopup()">✕</button>`;
            html += `<h3>${station.name}</h3>`;
            html += `<div class="popup-caption">${station.caption || ''}</div>`;
            if (d.summary) html += `<div class="popup-section"><p>${d.summary}</p></div>`;
            if (d.years) html += `<div class="popup-section"><h4>Experience</h4><p>${d.years}</p></div>`;
            if (d.skills && d.skills.length) {
                html += `<div class="popup-section"><h4>Skills</h4><div class="popup-tags">`;
                d.skills.forEach(s => html += `<span class="badge-tag">${s}</span>`);
                html += `</div></div>`;
            }
            if (d.projects && d.projects.length) {
                html += `<div class="popup-section"><h4>Projects</h4><ul>`;
                d.projects.forEach(p => html += `<li>${p}</li>`);
                html += `</ul></div>`;
            }
            if (d.commands && d.commands.length) {
                html += `<div class="popup-section"><h4>Example Commands</h4>`;
                d.commands.forEach(c => html += `<code style="display:block;background:#111827;color:#e5e7eb;padding:4px 8px;border-radius:6px;margin-bottom:4px;font-size:0.8rem;">${c}</code>`);
                html += `</div>`;
            }
            if (d.github) html += `<div class="popup-section"><a href="${d.github}" target="_blank" style="color:#0369a1;font-weight:600;">View on GitHub →</a></div>`;
            return html;
        }

        function openPopup(index) {
            popup.innerHTML = buildPopupHtml(stations[index]);
            overlay.classList.add('open');
        }

        window.__closeRoadmapPopup = function () {
            overlay.classList.remove('open');
        };

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.classList.remove('open');
        });

        document.querySelectorAll('.station').forEach(el => {
            el.addEventListener('click', () => {
                const index = parseInt(el.dataset.index);
                moveBusTo(index);
                setTimeout(() => openPopup(index), 500);
            });
        });

        updateStationStates(0);
    }

    initRoadmap();
})();