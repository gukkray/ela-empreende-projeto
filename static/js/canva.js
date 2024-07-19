$(function(){
    $(".js-create").click(function(){
        $.ajax({
            // Corpo da função
            url: "js/criar",
            type: "get",
            dataType: "json",

            beforeSend: function(){
                $('#modal-canva').modal('show');
            },
            success: function(data){
                $('#modal-canva .modal-content').html(data.html_form);
            },
        });
    });
    $("#modal-canva").on("submit",".js-create-form", function(){
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                    $("#table-canva tbody").html(data.html_list);
                    $("#modal-canva").modal("hide");
                }else{
                    $("#modal-canva .modal-content").html(data.html_form)
                }
            }
        });
        return false
    });
});