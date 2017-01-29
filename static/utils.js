
function load_jobs(params, current_page) {
    jQuery.support.cors = true;

    $(".dim_screen").show();

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

            $(".dim_screen").hide();

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
                edit_link = ' onclick="job_details(' + item.pk + ');" '

                trHTML += '<tr id="jobs_item_' + item.pk + '">';
                trHTML += '<td>' + '<input type="checkbox" class="view_checkbox" id="jobs_' + item.pk  + '">';
                trHTML += '<td ' + edit_link + '>' + item.pk;
                trHTML += '<td ' + edit_link + '>' + action_mapper[item.fields.action];
                trHTML += '<td ' + edit_link + '>' + item.fields.command;
                trHTML += '<td ' + edit_link + '>' + item.fields.created_at;
                trHTML += '<td ' + edit_link + '>' + item.fields.description;
                trHTML += '<td ' + edit_link + '>' + item.fields.path;
                trHTML += '<td ' + edit_link + '>' + item.fields.parameters;
                trHTML += '</tr>' ;
            });

            $('#jobs').append(trHTML);
        },

        error: function (msg) {
            alert(msg.responseText);
        }
    });
}

function job_details(job) {
    window.location.href = '/dashboard/jobs/' + job + '/';
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

