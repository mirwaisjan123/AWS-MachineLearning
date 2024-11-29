$("#prediction-form").submit(function (e) {
    e.preventDefault(); // Prevent form refresh
    const company = $("#company").val(); // Get selected company
    const days = parseInt($("#days").val()); // Get number of days to predict

    $.ajax({
        url: "/predict",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ company, days }),
        success: function (response) {
            const predictions = response.predictions;
            const historicalData = response.historical_data;
        
            // Create x-axis labels for historical and predicted data
            const labels = Array.from(
                { length: historicalData.length + predictions.length },
                (_, i) => `Day ${i + 1}`
            );
        
            // Combine data, leaving a gap for predictions
            const combinedHistoricalData = historicalData.concat(
                Array(predictions.length).fill(null)
            );
            const combinedPredictedData = Array(historicalData.length)
                .fill(null)
                .concat(predictions);
        
            // Render chart using Chart.js
            const ctx = document.getElementById("predictionChart").getContext("2d");
        
            new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Historical Prices",
                            data: combinedHistoricalData,
                            borderColor: "blue",
                            fill: false,
                        },
                        {
                            label: "Predicted Prices",
                            data: combinedPredictedData,
                            borderColor: "red",
                            fill: false,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Days",
                            },
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Stock Price",
                            },
                        },
                    },
                },
            });
        },
        error: function (error) {
            console.error("Error response from server:", error);
            alert(`Error: ${error.responseJSON.error}`);
        },
    });
});
