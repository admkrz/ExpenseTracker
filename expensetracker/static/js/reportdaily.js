function drawDailyChart(dailyLabels, dailyExpenseData, dailyIncomeData) {
    var ctxIncome = document.getElementById('dailyIncomeChart').getContext('2d');
    var chartIncome = new Chart(ctxIncome, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
            labels: dailyLabels,
            datasets: [{
                label: 'Daily Incomes',
                fill: false,
                lineTension: 0.1,
                backgroundColor: 'rgba(0, 102, 0, 1)',
                borderColor: 'rgba(0, 51, 0, 1)',
                data: dailyIncomeData
            }]
        },

        // Configuration options go here
        options: {}
    });

    var ctxExpense = document.getElementById('dailyExpenseChart').getContext('2d');
    var chartExpense = new Chart(ctxExpense, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
            labels: dailyLabels,
            datasets: [{
                label: 'Daily Expenses',
                fill: false,
                lineTension: 0.1,
                backgroundColor: 'rgba(255, 128, 0, 1)',
                borderColor: 'rgba(204, 102, 0, 1)',
                data: dailyExpenseData
            }]
        },

        // Configuration options go here
        options: {}
    });
}

$('#dailyExpenses').DataTable({
    "pagingType": "full_numbers",
    "order": [[3, "desc"]],
    "scrollY": "300px",
    "scrollCollapse": true,
    "paging": false,
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel'
    ]
});

$('#dailyIncomes').DataTable({
    "pagingType": "full_numbers",
    "order": [[3, "desc"]],
    "scrollY": "300px",
    "scrollCollapse": true,
    "paging": false,
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel'
    ]
});