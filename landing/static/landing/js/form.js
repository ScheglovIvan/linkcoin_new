$( document ).ready(function() {
    $("form input[type='submit']").click(function(){
            form = $(this).parent("form")

            form_id = "#"+form.attr('id')

            if(form.attr('action') == undefined || form.attr('action') == ""){
                action = $(location).attr('href');
            }else{
                action = form.attr('action')
            }
            
			sendAjaxForm(form_id, action);
			return false; 
		}
    );
    $(document).on('click', function(e){
        var target = $(e.target);
            
        if ($(target).hasClass("overlay")){
            $(target).find(".modal").each( function(){
                $(this).removeClass("open");
            });
            setTimeout( function(){
                $(target).removeClass("open");
            }, 350);
        }
            
    });

    $("#goLogin").on('click', function(e){
        $(location).attr('href',window.location.origin + "/login");
    });

    $("form input[type='text'], form input[type='password']").on('click', function(e){
        $(this).attr("style", "");
        $("form .error-email-message").attr("style", "");
        $("."+$(this).attr("data-error")).attr("style", "");
    });

    $(".new-pass-form #pass_1").focusout(function(){
        if($(this).val().length < 8 && $(this).val().length > 0){
            $("."+$(this).attr("data-error")).attr("style", "opacity: 0.7!important")
            $(this).attr("style", "background: pink!important")
        }
        if($(this).val() != $(".new-pass-form #pass_2").val() && $(".new-pass-form #pass_2").val().length > 0){
            $("."+$(".new-pass-form #pass_2").attr("data-error")).attr("style", "opacity: 0.7!important")
            $(".new-pass-form #pass_2").attr("style", "background: pink!important")
        }
    });
    $(".new-pass-form #pass_2").focusout(function(){
        if($(this).val() != $(".new-pass-form #pass_1").val() && $(this).val().length > 0){
            $("."+$(this).attr("data-error")).attr("style", "opacity: 0.7!important")
            $(this).attr("style", "background: pink!important")
        }
    });
});
 
function sendAjaxForm(form_id, action) {
    $.ajax({
        url:     action, //url страницы (action_ajax_form.php)
        type:     "POST", //метод отправки
        dataType: "html", //формат данных
        data: $(form_id).serialize(),  // Сеарилизуем объект
        success: function(response) { //Данные отправлены успешно
            $(".modal").parents(".overlay").addClass("open");
            setTimeout( function(){
                $(".modal").addClass("open");
            }, 350);
            setTimeout( function(){
                if (window.location.href.split("/")[4] == "change_password"){
                    $(location).attr('href',window.location.origin + "/login");
                }
            }, 2500);
            if (window.location.href.split("/")[3] == "login"){
                $(location).attr('href',window.location.origin + "/login");
            }
    	},
        error: function(response) { // Данные не отправлены
            if(window.location.href.split("/")[3] == "register"){
                if(response.status == 400){
                    $(".already-use-email").attr("style", "opacity: 0.7!important")
                    $("#reg-email").attr("data-error", "already-use-email")
                }else if(response.status == 401){
                    $(".error-email").attr("style", "opacity: 0.7!important")
                    $("#reg-email").attr("data-error", "error-email")
                }else if(response.status == 402){
                    $(".error-len").attr("style", "opacity: 0.7!important")
                }else if(response.status == 403){
                    $(".error-match").attr("style", "opacity: 0.7!important")  
                }
            }
            $("form .error-email").attr("style", "opacity: 0.7!important;");
            $("form input[type='text']").attr("style", "background: pink!important");

            if (window.location.href.split("/")[3] == "login"){
                $("form input[type='text'], form input[type='password']").attr("style", "background: pink!important;");
                $(".error-login").attr("style", "opacity: 0.7!important;");
            }

            var inputs = $("form input[type='password'], form input[type='text']").length
            for(i=0; i < inputs; i++){
                if($("form input[type='password'], form input[type='text']").eq(i).val() == ""){
                    var error =  $("form input[type='password'], form input[type='text']").eq(i).attr("data-error")

                    $("form input[type='password'], form input[type='text']").eq(i).attr("style", "background: pink!important")
                    $("."+error).attr("style", "opacity: 0.7!important")
                }
            }
    	}
 	});
}