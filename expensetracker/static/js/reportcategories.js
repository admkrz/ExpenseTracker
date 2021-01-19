function drawCategoriesChart(incomeCategories, expenseCategories) {

    google.charts.load("current", {packages: ["corechart"]});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var incomeCategoriesData = incomeCategories;
        var incomeData = google.visualization.arrayToDataTable(incomeCategoriesData);

        var expenseCategoriesData = expenseCategories;
        var expenseData = google.visualization.arrayToDataTable(expenseCategoriesData);

        var options = {
            legend: {position: 'top'},
            fontSize: 14
        };

        var expenseChartDiv = document.getElementById('donutchartExpense');
        var expenseChartDownloadDiv = document.getElementById('donutchartExpenseDownload');
        var expenseChart = new google.visualization.PieChart(expenseChartDiv);

        // Wait for the chart to finish drawing before calling the getImageURI() method.
        google.visualization.events.addListener(expenseChart, 'ready', function () {
            expenseChartDownloadDiv.innerHTML = '<img id="expenseChartImg" src="' + expenseChart.getImageURI() + '">';
            expenseChartDownloadDiv.hidden = true;
        });

        expenseChart.draw(expenseData, options);

        var incomeChartDiv = document.getElementById('donutchartIncome');
        var incomeChartDownloadDiv = document.getElementById('donutchartIncomeDownload');
        var incomeChart = new google.visualization.PieChart(incomeChartDiv);

        // Wait for the chart to finish drawing before calling the getImageURI() method.
        google.visualization.events.addListener(incomeChart, 'ready', function () {
            incomeChartDownloadDiv.innerHTML = '<img id="incomeChartImg" src="' + incomeChart.getImageURI() + '">';
            incomeChartDownloadDiv.hidden = true;
        });

        incomeChart.draw(incomeData, options);
    }

}

function drawCategoriesChartIndex(incomeCategories, expenseCategories) {

    google.charts.load("current", {packages: ["corechart"]});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var incomeCategoriesData = incomeCategories;
        var incomeData = google.visualization.arrayToDataTable(incomeCategoriesData);

        var expenseCategoriesData = expenseCategories;
        var expenseData = google.visualization.arrayToDataTable(expenseCategoriesData);

        var options = {
            legend: {position: 'top'},
            fontSize: 14
        };

        var expenseChartDiv = document.getElementById('donutchartExpense');
        var expenseChart = new google.visualization.PieChart(expenseChartDiv);

        expenseChart.draw(expenseData, options);

        var incomeChartDiv = document.getElementById('donutchartIncome');
        var incomeChart = new google.visualization.PieChart(incomeChartDiv);

        incomeChart.draw(incomeData, options);
    }

}

if (document.getElementById("downloadCategoriesExpenseJPG") != null) {
    document.getElementById("downloadCategoriesExpenseJPG").addEventListener('click', function () {
        var expenseChart = document.getElementById('expenseChartImg');

        var imgUri = expenseChart.src;

        var a = document.getElementById("downloadCategoriesExpenseJPG");
        /*insert chart image url to download button (tag: <a></a>) */
        a.href = imgUri;
    });
}

if (document.getElementById("downloadCategoriesExpensePNG") != null) {
    document.getElementById("downloadCategoriesExpensePNG").addEventListener('click', function () {
        var expenseChart = document.getElementById('expenseChartImg');

        var imgUri = expenseChart.src;

        var a = document.getElementById("downloadCategoriesExpensePNG");
        /*insert chart image url to download button (tag: <a></a>) */
        a.href = imgUri;
    });
}

if (document.getElementById("downloadCategoriesIncomeJPG") != null) {
    document.getElementById("downloadCategoriesIncomeJPG").addEventListener('click', function () {
        var expenseChart = document.getElementById('incomeChartImg');

        var imgUri = expenseChart.src;

        var a = document.getElementById("downloadCategoriesIncomeJPG");
        /*insert chart image url to download button (tag: <a></a>) */
        a.href = imgUri;
    });
}

if (document.getElementById("downloadCategoriesIncomePNG") != null) {
    document.getElementById("downloadCategoriesIncomePNG").addEventListener('click', function () {
        var expenseChart = document.getElementById('incomeChartImg');

        var imgUri = expenseChart.src;

        var a = document.getElementById("downloadCategoriesIncomePNG");
        /*insert chart image url to download button (tag: <a></a>) */
        a.href = imgUri;
    });
}