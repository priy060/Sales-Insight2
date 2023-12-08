document.addEventListener('DOMContentLoaded', function () {
    const chartList = document.getElementById('chartList');
    const chartHistory = JSON.parse('{{ chart_history | tojson | safe }}');

    displayChartHistory(chartHistory, chartList);

    // Handle chart deletion
    chartList.addEventListener('click', function (event) {
        if (event.target.tagName === 'BUTTON') {
            const index = event.target.dataset.index;
            deleteChart(index, chartHistory, chartList);
        }
    });
});

function displayChartHistory(chartHistory, chartList) {
    chartList.innerHTML = '';

    chartHistory.forEach((chart, index) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <p>${chart.title}</p>
            <img src="${chart.plot_url}" alt="${chart.title}">
            <button data-index="${index}">Delete</button>
        `;
        chartList.appendChild(listItem);
    });
}

function deleteChart(index, chartHistory, chartList) {
    // Remove the chart at the specified index
    chartHistory.splice(index, 1);

    // Update local storage (or server-side session)
    // Since we're using Flask session, this step may not be necessary
    // localStorage.setItem('chartHistory', JSON.stringify(chartHistory));

    // Refresh the displayed chart history
    displayChartHistory(chartHistory, chartList);
}
