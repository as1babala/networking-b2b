
    $("#industry").change(function () {
      var url = $("#sector").attr("ajax_load_sectors");  // get the url of the `load_sectors` view
      var industryId = $(this).val();  // get the selected industry ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-sectors/)
        data: { 'industry_id': industryId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_sectors` view function
          console.log(data);
          $("sectors").html(data);  // replace the contents of the sector input with the data that came from the server
        }
      });

    });
