// Setting sort to what selected after reloading the page
key_values_now = document.location.search.substr(1).split("&");

// display date and time with moment
$(".moment-date").each((i, obj) => {
    var time = $(obj).text();
    $(obj).text(moment(time, "YYYYMMDDhhmm").fromNow());
});


for (var i = 0; i < key_values_now.length; i++) {
    if (key_values_now[i].startsWith("sort" + "=")) {
        value = key_values_now[i].split("=")[1];
        if (value.startsWith("-")) value = value.substring(1);
        $(`select option[value=${value}]`).attr("selected", true);
        break;
    }
}

const refreshWithParams = (params) => {
    document.location.search = params;
};

// add parms and refresh page
const addParamsAndRefresh = (key, value) => {

    let i = 0;
    for (; i < key_values_now.length; i++) {
        if (key_values_now[i].startsWith(key + "=")) {
            let pair = key_values_now[i].split("=");
            pair[1] = value;
            key_values_now[i] = pair.join("=");
            break;
        }
    }
    if (i >= key_values_now.length) {
        key_values_now[key_values_now.length] = [key, value].join("=");
    }
    refreshWithParams(key_values_now.join("&"));
}

// Select tage onchange handler
const handleSortChange = (element) => {
    key = encodeURIComponent("sort");
    sort_value = encodeURIComponent(
        element.options[element.selectedIndex].value
    );
    
    addParamsAndRefresh(key, sort_value);
};

// Sort order onclick listener 
const handleOnClick = () => {
    for (var i = 0; i < key_values_now.length; i++) {
        if (key_values_now[i].startsWith("sort" + "=")) {
            let pair = key_values_now[i].split("=");
            if (pair[1].startsWith("-")) {
                pair[1] = pair[1].substring(1);
            } else {
                pair[1] = "-" + pair[1];
            }
            key_values_now[i] = pair.join("=");
            break;
        }
    }
    refreshWithParams(key_values_now.join("&"));
};

// fun used to get csrf token

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// var csrftoken = getCookie('csrftoken');