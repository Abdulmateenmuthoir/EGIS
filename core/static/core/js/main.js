/* ═══════════════════════════════════════════════════════════
   EGIS File Manager — Main JavaScript
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Sidebar Toggle (Mobile) ────────────────────────────
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            sidebarOverlay.classList.toggle('active');
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('active');
        });
    }

    // ─── Auto-dismiss Toasts ────────────────────────────────
    const toasts = document.querySelectorAll('.toast[data-auto-dismiss]');
    toasts.forEach((toast, index) => {
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.4s ease forwards';
            setTimeout(() => toast.remove(), 400);
        }, 4000 + index * 500);
    });

    // Add slideOut animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut {
            to { opacity: 0; transform: translateX(40px); }
        }
    `;
    document.head.appendChild(style);

    // ─── Confirm before delete ──────────────────────────────
    const deleteButtons = document.querySelectorAll('.btn-icon-danger[title="Delete"]');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            // Don't prevent — let the user go to delete confirm page
        });
    });

    // ─── Staggered fade-in for table rows ───────────────────
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach((row, i) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(10px)';
        row.style.transition = `all 0.3s ease ${i * 0.03}s`;
        setTimeout(() => {
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, 50);
    });

    // ─── Stat card counter animation ────────────────────────
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(el => {
        const target = parseInt(el.textContent);
        if (isNaN(target)) return;
        el.textContent = '0';
        const duration = 1000;
        const step = target / (duration / 16);
        let current = 0;

        function animate() {
            current += step;
            if (current >= target) {
                el.textContent = target;
            } else {
                el.textContent = Math.floor(current);
                requestAnimationFrame(animate);
            }
        }
        requestAnimationFrame(animate);
    });

    // ─── Active nav link highlight ──────────────────────────
    // Already handled by Django template tags, but add smooth
    // scroll effect on click
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
