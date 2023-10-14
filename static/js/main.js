$.ajax({
    type: 'GET',
    url: 'enterprises/industry-json/',
    success: function(response){
        console.log(response.qs_industry)
    },
    error: function(error){
        console.log(error)
    }

})