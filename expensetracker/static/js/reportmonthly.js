function drawMonthlyChart(monthlyLabels, monthlyExpenseData, monthlyIncomeData) {
    var ctxMonthlyIncome = document.getElementById('monthlyIncomeChart').getContext('2d');
    var chartMonthlyIncome = new Chart(ctxMonthlyIncome, {
            // The type of chart we want to create
            type: 'bar',

            // The data for our dataset
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: 'Monthly Incomes',
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: 'rgba(0, 102, 0, 1)',
                    borderColor: 'rgba(0, 51, 0, 1)',
                    data: monthlyIncomeData
                }]
            },

            // Configuration options go here
            options: {}
        })
    ;

    var ctxMonthlyExpense = document.getElementById('monthlyExpenseChart').getContext('2d');
    var chartMonthlyExpense = new Chart(ctxMonthlyExpense, {
            // The type of chart we want to create
            type: 'bar',

            // The data for our dataset
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: 'Monthly Expenses',
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: 'rgba(255, 128, 0, 1)',
                    borderColor: 'rgba(204, 102, 0, 1)',
                    data: monthlyExpenseData
                }]
            },

            // Configuration options go here
            options: {}
        })
    ;
}

$('#monthlyExpenses').DataTable({
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

$('#monthlyIncomes').DataTable({
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