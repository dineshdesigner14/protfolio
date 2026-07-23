(function () {
    function init() {
        const container = document.getElementById('dworker-architecture');
        if (!container) { setTimeout(init, 200); return; }

        const bootOverlay = document.getElementById('arch-boot-overlay');
        const bootText = document.getElementById('arch-boot-text');
        const archStage = document.getElementById('arch-stage');
        const tooltip = document.getElementById('arch-tooltip');
        const bootLines = window.ARCH_BOOT_SEQUENCE || [];

        let booted = false;

        function runBoot() {
            if (booted) return;
            booted = true;
            let i = 0;
            function showLine() {
                if (i >= bootLines.length) {
                    setTimeout(() => {
                        bootOverlay.classList.add('hidden');
                        archStage.classList.add('revealed');
                    }, 500);
                    return;
                }
                const line = document.createElement('div');
                line.className = 'boot-line';
                line.textContent = '> ' + bootLines[i];
                bootText.appendChild(line);
                i++;
                setTimeout(showLine, 550);
            }
            showLine();
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    runBoot();
                    observer.disconnect();
                }
            });
        }, { threshold: 0.25 });
        observer.observe(container);

        document.querySelectorAll('.arch-node[data-id]').forEach(node => {
            const id = node.dataset.id;

            node.addEventListener('mouseenter', () => {
                const line = document.getElementById('arch-line-' + id);
                const center = document.getElementById('arch-center');
                if (line) line.classList.add('active');
                node.classList.add('active');
                if (center) center.classList.add('active');

                document.querySelectorAll('.arch-node[data-id]').forEach(n => {
                    if (n !== node) n.classList.add('dimmed');
                });
                document.querySelectorAll('.arch-line').forEach(l => {
                    if (l !== line) l.classList.add('dimmed');
                });

                const rect = node.getBoundingClientRect();
                const containerRect = container.getBoundingClientRect();
                tooltip.innerHTML = `<strong>${node.dataset.name}</strong><p>${node.dataset.desc}</p>`;
                tooltip.style.left = (rect.left - containerRect.left + rect.width / 2) + 'px';
                tooltip.style.top = (rect.top - containerRect.top - 10) + 'px';
                tooltip.classList.add('visible');
            });

            node.addEventListener('mouseleave', () => {
                const line = document.getElementById('arch-line-' + id);
                const center = document.getElementById('arch-center');
                if (line) line.classList.remove('active');
                node.classList.remove('active');
                if (center) center.classList.remove('active');

                document.querySelectorAll('.arch-node[data-id]').forEach(n => n.classList.remove('dimmed'));
                document.querySelectorAll('.arch-line').forEach(l => l.classList.remove('dimmed'));

                tooltip.classList.remove('visible');
            });
        });
    }
    init();
})();