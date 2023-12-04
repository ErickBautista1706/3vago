document.addEventListener("DOMContentLoaded", function () {
    // Llama directamente a updateChart al cargar la página
    updateChart();
});

function updateChart() {
    var canvas = document.querySelector('#chartjs-bar-chart');
    Chart.getChart(canvas)?.destroy();

    // Aquí puedes colocar la lógica para obtener los datos directamente sin el selector de mes
    fetch("/reservations_chart")
        .then(response => response.json())
        .then(data => {
            console.log("Datos obtenidos:", data);
            var datosAgrupados = {};

            data.forEach(function (item) {
                var id_cbn = item.id_cbn;
                if (!datosAgrupados[id_cbn]) {
                    datosAgrupados[id_cbn] = item.cantidad_reservaciones;
                } else {
                    datosAgrupados[id_cbn] += item.cantidad_reservaciones;
                }
            });

            var id_cbn = Object.keys(datosAgrupados);
            var cantidad_reservaciones = Object.values(datosAgrupados);

            var ctx = canvas.getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: id_cbn,
                    datasets: [{
                        label: 'Reservations',
                        data: cantidad_reservaciones,
                        backgroundColor: 'rgb(75, 192, 192)',
                    }]
                },
                options: {
                    
                }
            });
        })
        .catch(error => {
            console.error("Error al obtener datos:", error);
        });
}
