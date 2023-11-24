document.addEventListener("DOMContentLoaded", function () {
    // Mock data (replace this with your actual data)
    const dataFromDatabase = {
        audio1: {
            happy: 10,
            sad: 15,
            angry: 5,
            calm: 20
        },
        audio2: {
            happy: 5,
            sad: 12,
            angry: 8,
            calm: 15
        },
        audio3: {
            happy: 8,
            sad: 18,
            angry: 7,
            calm: 10
        },
        audio4: {
            happy: 12,
            sad: 6,
            angry: 10,
            calm: 22
        }
    };

    const audioColumns = Object.keys(dataFromDatabase);

    // Generate a pie chart for each audio column
    audioColumns.forEach((audioColumn) => {
        const canvas = document.createElement("canvas");
        canvas.width = 100;
        canvas.height = 100;
        const pieChartContainer = document.getElementById("pieChartContainer");
        pieChartContainer.appendChild(canvas);

        const datasets = [{
            label: audioColumn,
            data: Object.values(dataFromDatabase[audioColumn]),
            backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
        }];

        const pieChart = new Chart(canvas.getContext("2d"), {
            type: "pie",
            data: {
                labels: Object.keys(dataFromDatabase[audioColumn]),
                datasets: datasets
            },
            options: {
                responsive: true,
                legend: {
                    position: "bottom"
                }
            }
        });
    });
});
