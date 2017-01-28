
function load_jobs(params, current_page) {
    jQuery.support.cors = true;

    $("#jobs").innerHTML = "";

    $.ajax(
    {
        type: "GET",
        url: "/api/jobs/",
        data: params,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        cache: false,
        success: function (data, status, xhr) {

            total_pages = parseInt(xhr.getResponseHeader('total_pages')) + 1;

            $("#total_pages").val(total_pages);

            if(total_pages == current_page) {
                $("#next-link").hide();
            }
            else {
                $("#next-link").show();
            }

            for (i = 1; i <= total_pages; i++) {
                if(i == current_page) {
                    $("#page_selector").append("<option value=" + i + " selected>" + i + "</option>");
                }
                else {
                    $("#page_selector").append("<option value=" + i + ">" + i + "</option>");
                }
            }

            action_mapper = {'0': 'ssh',
                             '1': 'http',
                             '2': 'agent'}

            var trHTML = '';

            $.each(data, function (i, item) {
                trHTML += '<tr>' ;
                trHTML += '<td>' + item.pk;
                trHTML += '<td>' + action_mapper[item.fields.action];
                trHTML += '<td>' + item.fields.command;
                trHTML += '<td>' + item.fields.created_at;
                trHTML += '<td>' + item.fields.description;
                trHTML += '<td>' + item.fields.path;
                trHTML += '<td>' + item.fields.parameters;
                trHTML += '</tr>' ;
            });

            $('#jobs').append(trHTML);

        },

        error: function (msg) {

            alert(msg.responseText);
        }
    });
}
