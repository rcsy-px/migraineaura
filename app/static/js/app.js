const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  document.documentElement.setAttribute("data-bs-theme", savedTheme);
}

document.querySelector("[data-theme-toggle]")?.addEventListener("click", () => {
  const next = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-bs-theme", next);
  localStorage.setItem("theme", next);
});

document.querySelectorAll("[data-range-output]").forEach((range) => {
  const output = document.getElementById(range.dataset.rangeOutput);
  const sync = () => {
    if (output) output.textContent = range.value;
  };
  range.addEventListener("input", sync);
  sync();
});

const chartCanvas = document.getElementById("intensityChart");
if (chartCanvas && window.Chart) {
  const points = JSON.parse(chartCanvas.dataset.points || "[]");
  new Chart(chartCanvas, {
    type: "line",
    data: {
      labels: points.map((point) => point.date),
      datasets: [{
        data: points.map((point) => point.intensity),
        borderColor: "#4f7f8f",
        backgroundColor: "rgba(79, 127, 143, .16)",
        fill: true,
        tension: .35,
        pointRadius: 3
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { min: 0, max: 4, ticks: { stepSize: 1 } } },
      responsive: true,
      maintainAspectRatio: false
    }
  });
}
