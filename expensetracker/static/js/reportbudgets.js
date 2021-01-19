function drawBudgetsChart(budgetLabels, budgetData) {
    if (document.getElementById('budgetsChart') != null) {
        var ctx = document.getElementById('budgetsChart').getContext('2d');
        var chart = new Chart(ctx, {
                // The type of chart we want to create
                type: 'line',

                // The data for our dataset
                data: {
                    labels: budgetLabels,
                    datasets: [{
                        label: 'Budgets Balance',
                        fill: false,
                        lineTension: 0.1,
                        backgroundColor: 'rgba(236, 43, 43, 1)',
                        borderColor: 'rgba(63, 191, 80, 1)',
                        data: budgetData
                    }]
                },

                // Configuration options go here
                options: {}
            })
        ;
    }
}

if (document.getElementById("downloadBudgetReportJPG") != null) {
    document.getElementById("downloadBudgetReportJPG").addEventListener('click', function () {
        /*Get image of canvas element*/
        var url_base64jp = document.getElementById("budgetsChart").toDataURL("image/jpg");
        /*get download button (tag: <a></a>) */
        var a = document.getElementById("downloadBudgetReportJPG");
        /*insert chart image url to download button (tag: <a></a>) */
        a.href = url_base64jp;
    });
}

if (document.getElementById("downloadBudgetReportPNG") != null) {
    document.getElementById("downloadBudgetReportPNG").addEventListener('click', function () {
        /*Get image of canvas element*/
        var url_base64jp = document.getElementById("budgetsChart").toDataURL("image/png");
        /*get download button (tag: <a></a>) */
        var a = document.getElementById("downloadBudgetReportPNG");
        /*insert chart image url to download button (tag: <a></a>) */
        a.href = url_base64jp;
    });
}