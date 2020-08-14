$( document ).ready(function() {
    $("form input[type='submit']").click(function(){
            form = $(this).parent("form")

            form_id = "#"+form.attr('id')

            if(form.attr('action') == undefined || form.attr('action') == ""){
                action = $(location).attr('href');
            }else{
                action = form.attr('action')
            }
            
            var parent_el = $("#body")

            createLoader(parent_el)
			sendAjaxForm(form_id, action, parent_el);
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
 
function sendAjaxForm(form_id, action, parent_el) {
    $.ajax({
        url:     action, //url страницы (action_ajax_form.php)
        type:     "POST", //метод отправки
        dataType: "html", //формат данных
        data: $(form_id).serialize(),  // Сеарилизуем объект
        success: function(response) { //Данные отправлены успешно
            $(".modal").parents(".overlay").addClass("open");
            setTimeout( function(){
                parent_el.children(".loader_background").remove()
                $(".modal").addClass("open");
            }, 350);
            setTimeout( function(){
                if (window.location.href.split("/")[4] == "change_password"){
                    $(location).attr('href',window.location.origin + "/login");
                }
            }, 2500);
    	},
        error: function(response) { // Данные не отправлены
            setTimeout(function (){
                parent_el.children(".loader_background").remove()
            }, 300);
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

function createLoader(parent_el){
    parent_el.append('<div class="loader_background"><section><div class="sk-fading-circle"><div class="sk-circle sk-circle-1"></div><div class="sk-circle sk-circle-2"></div><div class="sk-circle sk-circle-3"></div><div class="sk-circle sk-circle-4"></div><div class="sk-circle sk-circle-5"></div><div class="sk-circle sk-circle-6"></div><div class="sk-circle sk-circle-7"></div><div class="sk-circle sk-circle-8"></div><div class="sk-circle sk-circle-9"></div><div class="sk-circle sk-circle-10"></div><div class="sk-circle sk-circle-11"></div><div class="sk-circle sk-circle-12"></div></div></section></div>');  
}