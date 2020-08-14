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

    $("#goLogin").on('click', function(e){
        $(location).attr('href',window.location.origin + "/login");
    });

    $("form input[type='text'], form input[type='password'], label").on('click', function(e){
        $(this).attr("style", "");
        $("."+$(this).attr("data-error")).attr("style", "");
    });
});
 
function sendAjaxForm(form_id, action, parent_el) {
    $.ajax({
        url:     action, //url страницы (action_ajax_form.php)
        type:     "POST", //метод отправки
        dataType: "html", //формат данных
        data: $(form_id).serialize(),  // Сеарилизуем объект
        success: function(response) { //Данные отправлены успешно
            setTimeout( function(){
                console.log(response.status)
                parent_el.children(".loader_background").remove()
                $(".overlay").addClass("open");
                $(".modal").addClass("open");
            }, 350);
    	},
        error: function(response) { // Данные не отправлены
            setTimeout(function (){
                parent_el.children(".loader_background").remove()
            }, 300);
            if(response.status == 400){
                $(".already-use-email").attr("style", "opacity: 0.7!important")
                $("#reg-email").attr("data-error", "already-use-email")
                $("#reg-email").attr("style", "background: pink")
            }else if(response.status == 401){
                $(".error-email").attr("style", "opacity: 0.7!important")
                $("#reg-email").attr("data-error", "error-email")
                $("#reg-email").attr("style", "background: pink")
            }else if(response.status == 402){
                $(".error-len").attr("style", "opacity: 0.7!important")
                $("#reg-pass").attr("style", "background: pink")
            }else if(response.status == 403){
                $(".error-match").attr("style", "opacity: 0.7!important") 
                $("#reg-pass-repeat").attr("style", "background: pink")
            }else if(response.status == 404){
                $(".error-checkbox").attr("style", "opacity: 0.7!important") 
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

function createLoader(parent_el){
    parent_el.append('<div class="loader_background"><section><div class="sk-fading-circle"><div class="sk-circle sk-circle-1"></div><div class="sk-circle sk-circle-2"></div><div class="sk-circle sk-circle-3"></div><div class="sk-circle sk-circle-4"></div><div class="sk-circle sk-circle-5"></div><div class="sk-circle sk-circle-6"></div><div class="sk-circle sk-circle-7"></div><div class="sk-circle sk-circle-8"></div><div class="sk-circle sk-circle-9"></div><div class="sk-circle sk-circle-10"></div><div class="sk-circle sk-circle-11"></div><div class="sk-circle sk-circle-12"></div></div></section></div>');  
}