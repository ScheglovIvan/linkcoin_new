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
    $("form input[type='text'], form input[type='password']").on('click', function(e){
        $(this).attr("style", "");
        $("form .error-email-message").attr("style", "");
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
            $(location).attr('href',window.location.origin + "/login");
    	},
        error: function(response) { // Данные не отправлены
            setTimeout(function (){
                $("form input[type='text'], form input[type='password']").attr("style", "background: pink!important;");
                $(".error-login").attr("style", "opacity: 0.7!important;");
                parent_el.children(".loader_background").remove()
            }, 300);
    	}
 	});
}

function createLoader(parent_el){
    parent_el.append('<div class="loader_background"><section><div class="sk-fading-circle"><div class="sk-circle sk-circle-1"></div><div class="sk-circle sk-circle-2"></div><div class="sk-circle sk-circle-3"></div><div class="sk-circle sk-circle-4"></div><div class="sk-circle sk-circle-5"></div><div class="sk-circle sk-circle-6"></div><div class="sk-circle sk-circle-7"></div><div class="sk-circle sk-circle-8"></div><div class="sk-circle sk-circle-9"></div><div class="sk-circle sk-circle-10"></div><div class="sk-circle sk-circle-11"></div><div class="sk-circle sk-circle-12"></div></div></section></div>');  
}