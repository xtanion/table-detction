$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "static/js/final.csv",
        dataType: "text",
        success: function (data) {
            var table = "<table>";
            var rows = data.split("\n");

            rows.forEach(function (row) {
                var cells = row.split(",");

                if (cells.length > 1) {
                    table += "<tr>";
                    cells.forEach(function (cell) {
                        table += "<td>" + cell + "</td>";
                    });
                    table += "</tr>";
                }
            });

            table += "</table>";
            $("#csvTable").html(table);
        },
    });
});
