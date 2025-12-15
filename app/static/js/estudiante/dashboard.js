console.log("Dashboard JS cargado correctamente");

// ==========================
// GRÁFICA RADAR
// ==========================
const radarCtx = document.getElementById("radarChart");

if (radarCtx) {
    new Chart(radarCtx, {
        type: "radar",
        data: {
            labels: ["RM", "LC", "CN", "EN", "CC"],
            datasets: [
                {
                    label: "Desempeño",
                    data: [60, 75, 55, 80, 65], // 🔥 Datos de ejemplo
                    backgroundColor: "rgba(26, 157, 143, 0.3)",
                    borderColor: "rgba(26, 157, 143, 1)",
                    borderWidth: 2,
                }
            ]
        },
        options: {
            scales: {
                r: {
                    angleLines: { color: "#ddd" },
                    grid: { color: "#ddd" },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
}


// ==========================
// MINI GAUGES
// ==========================
function miniGauge(canvasId, value) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Progreso", "Restante"],
            datasets: [
                {
                    data: [value, 100 - value],
                    backgroundColor: ["#1A9D8F", "#E0E0E0"],
                    borderWidth: 0,
                }
            ]
        },
        options: {
            cutout: "70%",
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}

miniGauge("gaugeRM", 60);
miniGauge("gaugeLC", 75);
miniGauge("gaugeCN", 55);
miniGauge("gaugeEN", 80);
miniGauge("gaugeCC", 65);


// ==========================
// PROGRESO SEMANAL (LINE CHART)
// ==========================
const progressCtx = document.getElementById("progressChart");

if (progressCtx) {
    new Chart(progressCtx, {
        type: "line",
        data: {
            labels: ["Semana 1", "Semana 2", "Semana 3", "Semana 4"],
            datasets: [
                {
                    label: "Progreso",
                    data: [40, 55, 60, 75],
                    borderColor: "#1A9D8F",
                    backgroundColor: "rgba(26, 157, 143, 0.3)",
                    fill: true,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { suggestedMin: 0, suggestedMax: 100 }
            }
        }
    });
}
