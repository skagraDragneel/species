$("#detectBtn").click(function() {
    imageData = {
        image_data: $("#photo").attr("src")
    }
    $.ajax({
        type: "POST",
        url: "get_name",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(imageData),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){alert(data);},
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
})