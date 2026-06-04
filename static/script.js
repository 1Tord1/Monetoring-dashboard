// Hent oppdatert data fra API og oppdater siden hver sekund
setInterval(async () => {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        // Oppdater alle elementer på siden med ny data
        document.querySelectorAll('[data-field="current_time"]').forEach(el => {
            el.textContent = data.current_time;
        });
        document.querySelectorAll('[data-field="cpu_percent"]').forEach(el => {
            el.textContent = data.cpu_percent + ' %';
        });
        document.querySelectorAll('[data-field="ram_total_gb"]').forEach(el => {
            el.textContent = data.ram_total_gb + ' GB';
        });
        document.querySelectorAll('[data-field="ram_used_gb"]').forEach(el => {
            el.textContent = data.ram_used_gb + ' GB / ' + data.ram_percent + ' %';
        });
    } catch (error) {
        console.error('Feil ved henting av stats:', error);
    }
}, 1000);

