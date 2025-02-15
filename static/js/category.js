$(document).ready(function () {
    // Simulating page load delay (remove this in real use)
    setTimeout(function () {
        $("#loader-wrapper").fadeOut("slow", function () {
            $("#content").fadeIn();
        });
    }, 2000); // 2-second delay for demonstration
});

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

function searchfetch(){
    searchval = $('#search-bar').val()  
    $.ajax({
        url: "http://127.0.0.1:8000/fetchbooksearch/",  // Change this to your API URL
        method: "POST", 
        headers: { "X-CSRFToken": getCSRFToken() },           
        data: { "searchval":  searchval },
        "timeout": 0,
        dataType: "json",
        beforeSend: function () { 
            $("#loader-wrapper").show()
        },
        success: function (response) {
            bookdata = response['bookdata']
            updatefetched_data(bookdata,'search')
            $("#loader-wrapper").hide()
        },
        error: function () {
            console.log('Stopped from fetching')
            $("#loader-wrapper").hide()
        }
    });

}

function openpopup(url){
    if(url=="None"){
        swal("No viewable version available") 
        return false
    }else{
        window.open(url, '_blank');
    }
}

function updatefetched_data(bookdata,categorytype=''){    
    if(categorytype=='search'){ 
        $('#scrollload').html('')
        if(bookdata.length == 0){
            $('#scrollload').html(`
                <div class="container error-container"> 
                    <div class="error-message">Books Not Available</div>
                    <p>Sorry, Please check with another category/Search.</p>
                    <a href="/" class="btn btn-primary">Go to Homepage</a>
                </div>`)
        }
    }  

    for (vals of bookdata){
        try{                                
            authorname = vals['authors'][0]
            authorval = authorname['name']
        }catch(err) {
            authorval = ''
        }
        if(vals['img']){
            $('#scrollload').append(`<div class="col-md-6 col-lg-2 cardcontent"  onclick="openpopup('${vals['srclink']}')">
                                    <div class="book-card" style="width: 100%;"> 
                                        <img src="${vals['img']}" alt="Book"> 
                                        <p class="mt-2 fw-bold text-paragraph" data-bs-toggle="tooltip" data-bs-placement="right" title="${vals['fulltitle']}">${vals['title']}</p>
                                        <p class="text-muted">
                                            ${authorval}
                                        </p>
                                    </div>
                                </div>`)
        }
    }
}

$(document).ready(function () {
    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 10) {  
            // AJAX Call when user reaches the bottom
            $.ajax({
                url: "http://127.0.0.1:8000/fetchbooksscroll/",  // Change this to your API URL
                method: "GET",
                "timeout": 0,
                dataType: "json",
                beforeSend: function () {
                    //on before send
                    $("#loader-wrapper").show()
                },
                success: function (response) {
                    bookdata = response['bookdata']
                    updatefetched_data(bookdata)
                    $("#loader-wrapper").hide()
                },
                error: function () {
                    console.log('Stopped from fetching')
                    $("#loader-wrapper").hide()
                }
            });
        }
    });
});