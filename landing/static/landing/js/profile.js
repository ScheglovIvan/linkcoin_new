$( document ).ready(function() {
  if($(window).width() < 550){

  }
  if($(window).width() < 500){
    $("#change_pass_settings .payment-method_header").attr("data-height", "300px")

    // payment_method_settings_h = (parseInt($("#payout_method_settings .payment-method_header").attr("data-height").split("px")[0]) + 80).toString() + "px"
    payment_method_settings_h = (parseInt($("#payout_method_settings .payment-method_header").attr("data-height").split("px")[0]) + 130).toString() + "px"
    $("#payout_method_settings .payment-method_header").attr("data-height", payment_method_settings_h)

  }
  if($(window).width() < 421){
    var el = $("#payout_method_settings .payment-method_header")

    var height = (parseInt(el.attr("data-height").split("px")[0]) + 60).toString() + "px"
    el.attr("data-height", height)
  }


  var tab, tabContent;
	tabContent = document.getElementsByClassName("profile__tabContent");
	tab = document.getElementsByClassName("profile__tab");
	hideTabsContent(1);

	function hideTabsContent(a) {
		for(var i = a; i<tabContent.length; i++) {
			tabContent[i].classList.remove("show");
			tabContent[i].classList.add("hide");
		}
  }
  $("#add_payout_method .payout_method_container").click(function(){
    $("#add_payout_method label[for='recipient']").html($(this).attr("data-name"))
  });
  $("body").on("click", "#ref_link_settings .ref_link_copy_continer", function () {
    input = $(this).parent().children(".ref_link_input");
    input.removeAttr("disabled")
    input.select();
    try { 
      document.execCommand('copy'); 
    } catch(err) { 
      console.log('Can`t copy, boss'); 
    }
    window.getSelection().removeAllRanges();
    input.attr("disabled", "")
  });


  $(".referal-input-conteiner i").click(function(){
    $(".referal-input").removeAttr("disabled")
    $(".referal-input").select();
    try { 
      document.execCommand('copy'); 
    } catch(err) { 
      console.log('Can`t copy, boss'); 
    }
    window.getSelection().removeAllRanges();
    $(".referal-input").attr("disabled", "")
  });
    
  $(".profile__1-month").click(function(){
      showDiagramInThisPeriod($(this))
      for(var i = 0; i<tab.length; i++) {
          tab[i].classList.remove("profile__dates-active");
      }
      this.classList.add("profile__dates-active");
  });

  $(".profile__3-month").click(function(){
      showDiagramInThisPeriod($(this))
      for(var i = 0; i<tab.length; i++) {
          tab[i].classList.remove("profile__dates-active");
      }
      this.classList.add("profile__dates-active");
  });

  $(".profile__6-month").click(function(){
      showDiagramInThisPeriod($(this))
      for(var i = 0; i<tab.length; i++) {
          tab[i].classList.remove("profile__dates-active");
      }
      this.classList.add("profile__dates-active");
  });

  $("body").on("click", "#payout_modal label .payout_method_item", function () {
    $("#payout_modal label .payout_method_item").attr("style", "")
    $(this).css("box-shadow", "inset 0px 0px 20px rgba(0, 117, 255, 0.2)")
  });

  $("#close_settings").click(function(){
    $("#settings_modal").removeClass("open")
    $(".overlay").removeClass("open")
  });

  $(".add_payout_method").click(function(){
    $("#payout_modal").removeClass("open")
    $("#settings_modal").addClass("open")
    $('#payout_method_settings .payment-method_header').trigger('click')
  });

  $(".close_get_payout").click(function(){
    $("#payout_modal").removeClass("open")
    $(".overlay").removeClass("open")
  });
  

  $("#create_ref_link_btn").click(function(){
    var form_id = "#create_ref_link"
    parent_el = $(this).parent().parent().parent()
    createLoader(parent_el)
    var del_item = parent_el.children(".loader_background")
    $.ajax({
      url:      window.location.origin + "/profile/create_ref_link",
      type:     "POST",
      dataType: "html",
      data: $(form_id).serialize(),
        success: function(response) {
          var ref_link = $(form_id).serialize().split("ref_link=")[1].split("&")[0]
          var full_link = window.location.origin + "?ref=" + ref_link
          $("#ref_link_settings .payout_method_list").append('<div class="payout_method_item" style="border: none; height: min-content; padding: 0; margin-top: 20px; border-radius: 3px 0 0 3px;"><div class="payout_method_content_inline"><div class="payout_method_item_content" style="width: 100%; margin: 0;"><div class="ref_link_content"><input class="ref_link_input" value="' + full_link + '" disabled><div class="ref_link_copy_continer"><i class="far fa-clone"></i></div></div></div></div></div>')
          $("#ref_link_settings .payment-method-form-container").height($("#ref_link_settings .payment-method-form-container").height()+58)
          setTimeout(function (){
            del_item.remove()
          }, 500);
        },
        error: function(response) {
          $("#ref_link_settings .remove_payout_method_info").attr("style", "opacity: 1;")
          $("#ref_link_settings .payment-method-form-container").height($("#ref_link_settings .payment-method-form-container").height()+64)
          if(response.status == 400){
            // $("#ref_link_settings .remove_payout_method_info h5").html("In order to add a new referral link, delete one of the existing ones. You can use up to three links at once.")
            $("#ref_link_settings .remove_payout_method_info h5").html("You are already using the maximum number of links. One user can use up to 3 links at the same time.")
            
          }else if(response.status == 401){
            $("#ref_link_settings .remove_payout_method_info h5").html("To create a referral link, use only Latin letters and numbers. Special characters and space are not allowed. '$#%^&*@#(_+)'")
          }else if(response.status == 402){
            $("#ref_link_settings .remove_payout_method_info h5").html("To create a referral link, use only Latin letters and numbers. Special characters and space are not allowed. '$#%^&*@#(_+)'")
          }else if(response.status == 403){
            $("#ref_link_settings .remove_payout_method_info h5").html("This referral link is already in use by another user. Try again. Use only latin letters and numbers.")
          }
          setTimeout(function (){
            del_item.remove()
          }, 500);
        }
      });
  });

  $(".make_payment_btn").click(function(){
    $("#payout_error_method_not_valid").remove()

    var parent_el = $("#payout_modal .modal-wrapper")
    createLoader(parent_el)

    var del_item = parent_el.children(".loader_background")

    var el_count = $("#payout_modal .payout_method_list label").length
    for(i = 0; i < el_count; i++){
      var el = $("#payout_modal .payout_method_list label:eq(" + i +") input[type='radio']")
      if(el.prop("checked")){
        var value = el.attr("data-value")
        break;
      }
    }
    var form_id = "#get_payout_form"
    $.ajax({
        url:      window.location.origin + "/profile/payout",
        type:     "POST",
        dataType: "html",
        data: $(form_id).serialize() + "&" + value,
        success: function(response) {
          $("#profile .profile__balance .amount-of-money").html("$0.0")
          $("#payout_modal .payout_counter_container").html('<i class="fas fa-shopping-cart" aria-hidden="true"></i>$0.0 USD')
          $(".payout_data_background .payout_data_container:eq(0) h5").html('$0.0 USD')

          $(".loader_background section").remove()
          parent_el.append('<div class="change_pass_success"><div class="popup-status"><i class="far fa-check-circle"></i><h1 class="title">Completed</h1></div><p>The money was sent to your wallet, which you selected above.</p><input type="button" class="modal-form-btn done-btn close_payout_modal" value="Ok"></div>')
        },
        error: function(response) {
          $("#payout_error_method_not_valid").remove()
          if(response.status == 403){
            $(".payout_error_container").append('<div class="remove_payout_method_info" id="payout_error_method_not_valid" style="opacity: 1;"><i class="fas fa-exclamation-triangle" aria-hidden="true"></i><h5>You have entered incorrect data, please select new data and try again. <a href="/policy/support" style="color: #0c77bd;">Learn more</a></h5></div>')
          }
          setTimeout(function (){
            del_item.remove()
          }, 500);
      }});
  });

  $("body").on("click", "#payout_modal .close_payout_modal", function () {
    $(".overlay").removeClass("open")
    $("#payout_modal").removeClass("open")
  });

  $(".withdraw-button").click(function(){
    $(".overlay").addClass("open")
    $("#payout_modal").addClass("open")

    $("#payout_modal .payout_method_list label").remove()
  
    var form_id = "#payout"
    $.ajax({
      url:      window.location.origin + "/profile/get_payout_method",
      type:     "GET",
      dataType: "json",
      success: function(response) {
        var data = response["data"]

        $(".payout_error_container #payout_error_method_not_found").remove()
        if(data.length == 0){
          var el_num = "0"
          if($(".payout_error_container").length == 2){
            var el_num = "1"
          }
          $(".payout_error_container:eq(" + el_num + ")").append('<div class="remove_payout_method_info" id="payout_error_method_not_found" style="opacity: 1;"><i class="fas fa-exclamation-triangle" aria-hidden="true"></i><h5>In order to receive money, add a payout method.</h5></div>')
        }

        for(method in data){
          name = data[method]["name"]
          recipient = data[method]["recipient"]
          def = data[method]["default"]

          var img = ""
          if(name == "PayPal"){
            img = "<img src='static/landing/images/profile/paypal_logo.png'>"
          }else if(name == "Venmo"){
            img = "<img src='static/landing/images/profile/venmo_logo.png'>"
          }else if(name == "BTC"){
            img = "<img src='static/landing/images/profile/BTC_Logo.svg'>"
          }

          if(def){
            var style = 'style="box-shadow: inset 0px 0px 20px rgba(0, 117, 255, 0.2)"'
            var check = "checked"
          }else{
            var style = ""
            var check = ""
          }

          if(def){
            $("#payout_modal .payout_method_list .payout_method_list_container").prepend('<label><div class="payout_method_item"' + style + '><div class="payout_method_content_inline"><div class="payout_method_item_logo">' + img + '</div><div class="payout_method_item_content"><h3 class="payout_method_title">' + name + '</h3><h5 class="payout_method_data">' + recipient + '</h5></div><input type="radio" name="payout_method" data-value="method=' + name + '&recipient=' + recipient + '"' + check + '/></div></div></label>')
          }else{
            $("#payout_modal .payout_method_list .payout_method_list_container").append('<label><div class="payout_method_item"' + style + '><div class="payout_method_content_inline"><div class="payout_method_item_logo">' + img + '</div><div class="payout_method_item_content"><h3 class="payout_method_title">' + name + '</h3><h5 class="payout_method_data">' + recipient + '</h5></div><input type="radio" name="payout_method" data-value="method=' + name + '&recipient=' + recipient + '"' + check + '/></div></div></label>')
          }
        }
      },
      error: function(response) {
        return false
    }});
  });

  $(".profile__all-time").click(function(){
      showDiagramInThisPeriod($(this))
      for(var i = 0; i<tab.length; i++) {
          tab[i].classList.remove("profile__dates-active");
      }
      this.classList.add("profile__dates-active");
  });

  $(".day-bar-stat").click(function(){
    var date = $(this).attr("data-date")

    if(date == ""){
      var year = 2040
      var month = 1
      var day = 1
    }else{
      var year = date.split("-")[0]
      var month = date.split("-")[1]
      var day = date.split("-")[2]
    }

    sendAjaxWeeklyStats(year, month, day)

    $(".today-bar-stat").removeClass("today-bar-stat")
    $(this).addClass("today-bar-stat")

    $(".profile__traffic-content").scrollTop(0);
    jQuery(".profile__traffic-content").animate({
      scrollTop: 999
    }, 1000);
    
  });

  function showDiagramInThisPeriod(el){
      if(el.attr("class").split(" ")[2] == "profile__dates-active"){
        return false;
      }else{
        $(".chart2").html(" ")
          
        $(".profile__dates-stats-circles ul").html("<li class='chart2 blue-chart clicks-number' data-percent=''><span>0</span><p>clicks</p></li><li class='chart2 orange-chart purchase-number' data-percent=''><span>0</span><p>purchase</p></li><li class='chart2 red-chart sign-up-number' data-percent=''><span>0</span><p>sign up</p></li>")
        period = parseInt(el.attr('data-period'))
        sendAjaxGraphic(period)
      }
  }

  // Открытие и закрытие форм в модальном окне
  $(".payment-method_header").click(function(){
    var height = $(this).attr("data-height")

    $(".payment-method_header").children(".angle-up").attr("style", "transform: rotate(45deg)")
    $(".payment-method-form-container").attr("style", "padding: 0rem; height: 0px;")

    $(this).attr("style", "padding: 0px")
    $(this).children(".angle-up").attr("style", "transform: rotate(-135deg)")
    $(this).parent().attr("style", "padding: 1rem")
    $(this).parent().children(".payment-method-form-container").attr("style", "height: "+ height +"; opacity: 1;")
  });

  $(".close_change-pass").click(function(){
    $("#old_pass").val("")
    $("#new_pass").val("")
    $("#reply_new_pass").val("")

    $("#old_pass").attr("style", "")
    $("#new_pass").attr("style", "")
    $("#reply_new_pass").attr("style", "")

    $(".payout_input_error").remove()

    $("#settings_modal .payment-method_header").children(".angle-up").attr("style", "transform: rotate(45deg)")
    $("#settings_modal .payment-method-form-container").attr("style", "padding: 0rem; height: 0px; opacity: 0;")

    $(this).parent().parent().parent().parent().children(".payment-method_header").attr("style", "padding: 0px")
  });

  $(".fa-cog").click(function(){
    $(".overlay").addClass("open")
    $("#settings_modal").addClass("open")
  });

  $("body").on("click", "#settings_modal .payout_method_remove", function () {
    var height = $(this).parent().parent().parent().parent().parent().parent(".payment-method-form-container").height()
    var max_height = parseInt($(this).parent().parent().parent().parent().parent().parent().parent().children(".payment-method_header").attr("data-height").substr(0, 3)) + 105
    if(height < max_height){
      height += 105
    }
    $(this).parent().parent().parent().parent().parent().parent(".payment-method-form-container").css("height", height.toString() + "px")

    // $(".payout_method_item").css("height", "106px")
    // $(".remove_payout_method_info").css("opacity", "0")
    $(this).parent().parent().parent().children(".remove_payout_method_info").css("opacity", "0")

    $(this).parent().parent().parent().parent().css("height", "211px")
    $(this).parent().parent().parent().parent().children(".remove_payout_method_info").css("opacity", "1")
  });

  $("body").on("click", ".close_payment_method_remove", function () {
    var height = $(this).parent().parent().parent().parent().parent().height() - 105
    $(this).parent().parent().parent().parent().parent().css("height", height.toString() + "px")
    $(this).parent().parent().parent().parent().parent().parent().children(".payment-method_header").attr("data-height", height.toString() + "px")

    $(this).parent().parent().parent().css("height", "106px")
    $(this).parent().parent().parent().children(".remove_payout_method_info").css("opacity", "0")
  });

  $("body").on("click", ".del_payment_method", function () {
    var height = $(this).parent().parent().parent().parent().parent().height() - 211
    $(this).parent().parent().parent().parent().parent().css("height", height.toString() + "px")
    $(this).parent().parent().parent().parent().parent().parent().children(".payment-method_header").attr("data-height", height.toString() + "px")

    $(this).parent().parent().parent().attr("style", "opacity: 0; height: 0; padding-top: 0; padding-bottom: 0;")
    var del_item = $(this).parent().parent().parent()

    setTimeout(function (){
      del_item.remove()
    }, 500);
    
    var $form = $(this).parent().parent()
    $.ajax({
      // url:      window.location.origin + "/payments/paypal/payout_method/remove",
      url:      window.location.origin + "/profile/payout_method/remove",
      type:     "POST",
      dataType: "html",
      data: $form.serialize(),
      success: function(response) {
        return true
      },
      error: function(response) {
        return false
      }
    });
  });
  
  $(".add_payment_method-btn").click(function(){
    var form_id = "#" + $(this).parent().parent().attr("id")

    var parent_el = $(this).parent().parent()
    createLoader(parent_el)

    var this_el = $(this)
    $.ajax({
      // url:      window.location.origin + "/payments/paypal/payout_method/add",
      url:      window.location.origin + "/profile/payout_method/add",
      type:     "POST",
      dataType: "html",
      data: $(form_id).serialize(),
      success: function(response) {
        var data = $(form_id).serialize()

        var recipient = $("#recipient").val()
        var method = data.split("payout_method=")[1].split("&")[0]

        if(method == "PayPal"){
          var payout_img_path = "/static/landing/images/profile/paypal_logo.png"
        }else if(method == "Venmo"){
          var payout_img_path = "/static/landing/images/profile/venmo_logo.png"
        }else if(method == "BTC"){
          var payout_img_path = "/static/landing/images/profile/BTC_Logo.svg"
        }

        $("#payout_method_settings .payout_method_list").append('<div class="payout_method_item" id="payout_method_new_item" style="height: 0; padding-bottom: 0; padding-top: 0; border: none;"><div class="payout_method_content_inline"><div class="payout_method_item_logo"><img src="' + payout_img_path + '"></div><div class="payout_method_item_content"><h3 class="payout_method_title">' + method + '</h3><h5 class="payout_method_data">' + recipient + '</h5><div class="payout_method_footer"><h6 class="payout_method_available">Available</h6><h6 class="payout_method_remove">Remove</h6></div></div></div><div class="remove_payout_method_info"><i class="fas fa-exclamation-triangle"></i><h5>Removing means you cannot use this payout method to receive funds</h5></div><form method="POST" id="remove_payment_method_form"><div class="form-inline"><input type="hidden" name="method" value="' + method + '"/><input type="hidden" name="recipient" value="' + recipient + '"/><input type="button" class="modal-form-btn done-btn del_payment_method" value="Remove" /><div class="modal-form-btn cancel-btn close_payment_method_remove">Cancel</div></div></form></div>')

        setTimeout(function (){
          var height = this_el.parent().parent().parent().height() + 106
          this_el.parent().parent().parent().parent().children(".payment-method_header").attr("data-height", height + "px")
          this_el.parent().parent().parent().css("height", height + "px")

          $("#payout_method_new_item").attr("style", "")
          $("#payout_method_new_item").attr("id", "")
          
          parent_el.children(".loader_background").remove()
          $("#recipient").val("")
          $("#confirm_recipient").val("")
        }, 500);
      },
      error: function(response) {
        $(".payout_input_error").remove()
        if(response.status == 400){
          this_el.parent().parent().children(".form-inline:eq(1)").children(".form-row:eq(0)").children("input").css("border-color", "#e62048")
          this_el.parent().parent().children(".form-inline:eq(1)").children(".form-row:eq(0)").append("<h6 class='payout_input_error'>Enter valid data</h6>")
        }else if(response.status == 401){
          this_el.parent().parent().children(".form-inline:eq(1)").children(".form-row:eq(1)").children("input").css("border-color", "#e62048")
          this_el.parent().parent().children(".form-inline:eq(1)").children(".form-row:eq(1)").append("<h6 class='payout_input_error'>Confirm your data</h6>")
        }else if(response.status == 402){
          this_el.parent().parent().children(".form-inline:eq(1)").children(".form-row:eq(0)").children("input").css("border-color", "#e62048")
          this_el.parent().parent().children(".form-inline:eq(1)").children(".form-row:eq(0)").append("<h6 class='payout_input_error'>You are already using this method.</h6>")
        }

        setTimeout(function (){        
          parent_el.children(".loader_background").remove()
        }, 500);
      }
    });
  });

  $("body").on("click", ".clear_form", function () {
    $("#recipient").val("")
    $("#confirm_recipient").val("")

    $("#recipient").attr("style", "")
    $("#confirm_recipient").attr("style", "")

    $(".payout_input_error").css("opacity", "0")
  });

  $("body").on("click", ".overlay input[type='text'], .overlay input[type='password']", function () {
    $(this).attr("style", "")
    $(this).parent().children("h6").css("opacity", "0")
  });

  $("body").on("click", "#change_pass_btn", function () {
    var parent_el = $(this).parent().parent()
    createLoader(parent_el)

    var form_id = "#change_pass-form"
    $.ajax({
      url:      window.location.origin + "/register/is_authenticated/change_password",
      type:     "POST",
      dataType: "html",
      data: $(form_id).serialize(),
      success: function(response) {
        setTimeout(function (){        
          $(".loader_background section").remove()
          parent_el.append('<div class="change_pass_success"><div class="popup-status"><i class="far fa-check-circle"></i><h1 class="title">Completed</h1></div><p>Your password has been successfully changed.</p><input type="button" class="modal-form-btn done-btn close_success_change_pass" value="Ok"></div>')
        }, 700);
      },
      error: function(response) {
        if(response.status == 400){
          if($("#old_pass").val() == ""){
            $("#old_pass").css("border-color", "#e62048")
            $("#old_pass").parent().append("<h6 class='payout_input_error'>Enter your password</h6>")
          }

          if($("#new_pass").val() == ""){
            $("#new_pass").css("border-color", "#e62048")
            $("#new_pass").parent().append("<h6 class='payout_input_error'>Enter new password</h6>")
          }

          if($("#reply_new_pass").val() == ""){
            $("#reply_new_pass").css("border-color", "#e62048")
            $("#reply_new_pass").parent().append("<h6 class='payout_input_error'>Reply new password</h6>")
          }
        }else if(response.status == 401){
          $("#old_pass").css("border-color", "#e62048")
          $("#old_pass").parent().append("<h6 class='payout_input_error'>Enter your password</h6>")
        }else if(response.status == 402){
          $("#reply_new_pass").css("border-color", "#e62048")
          $("#reply_new_pass").parent().append("<h6 class='payout_input_error'>Reply new password</h6>")
        }else if(response.status == 403){
          $("#new_pass").css("border-color", "#e62048")
          $("#new_pass").parent().append("<h6 class='payout_input_error'>Password must be at least 8 characters</h6>")
        }
        setTimeout(function (){        
          $(".loader_background").remove()
        }, 500);
      }
    });
  });
  
  $("body").on("click", ".close_success_change_pass", function () {
    $(".change_pass_success").remove()
    setTimeout(function (){        
      $("#old_pass").val("")
      $("#new_pass").val("")
      $("#reply_new_pass").val("")

      $(".loader_background").remove()
    }, 300);

    $(".payment-method_header").children(".angle-up").attr("style", "transform: rotate(45deg)")
    $(".payment-method-form-container").attr("style", "padding: 0rem; height: 0px;")
    window.location = window.location.href
  });

  $("body").on("click", ".show_pass", function () {
    if($(this).parent().parent().children("input").attr("type") == "password"){
      $(this).parent().parent().children("input").attr("type", "text")
      $(this).css("opacity", "0.9")
    }else if($(this).parent().parent().children("input").attr("type") == "text"){
      $(this).parent().parent().children("input").attr("type", "password")
      $(this).css("opacity", "0.6")
    }
  });
  


  var date = new Date()
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()

  sendAjaxWeeklyStats(year, month, day)
  sendAjaxGraphic(1)

});
function sendAjaxWeeklyStats(year, month, day){
  $.ajax({
    url:      window.location.origin + "/api/v1/counter/get_day_stats/" + year + "/" + month + "/" + day,
    type:     "GET",
    dataType: "json",
    success: function(response) {
      // console.log(response)
      DayStatsData(response)
    },
    error: function(response) {
      return response.status;
    }
  });
}
function sendAjaxGraphic(period) {
    $.ajax({
        url:      window.location.origin + "/api/v1/counter/get_monthly_stats/" + period,
        type:     "GET",
        dataType: "json",
        success: function(response) {
          var data = responseSort(response)
          // console.log(response)
          mainGraphic(data)
          showTotalData(response["data"]["total"], response["data"]["devices"])
      },
      error: function(response) {
        return response.status;
    	}
 	});
}

function mainGraphic(data){
    $("#chart").html(" ")

    var click = data["clicks"]
    var signup = data["signups"]
    var purchase = data["purchases"]


    var days = data["days"]

    var options = {
      chart: {
        toolbar: {
          show: true,
          offsetX: 0,
          offsetY: 0,
          tools: {
            download: false,
            selection: false,
            zoom: true,
            zoomin: false,
            zoomout: false,
            pan: false,
            reset: true,
          },
          autoSelected: 'zoom' 
        },
        height: 380,
        type: "area",
        offsetX: 0,
      },
      dataLabels: {
        enabled: false
      },
      series: [
        {
          name: "Clicks",
          data: click
        },
        {
          name: "Sing up",
          data: signup
        },
        {
          name: "Purchase",
          data: purchase
        }
      ],
      colors: ["#5348ad", "#ff327f", "#fbad37"],
      fill: {
          colors: ["#5348ad", "#ff327f", "#fbad37"],
        type: "gradient",
        gradient: {
          shadeIntensity: 1
        }
      },
      xaxis: {
          type: 'datetime',
          categories: days,
          labels: {
            rotate: 0,
            hideOverlappingLabels: true,
            maxHeight: 25,

            datetimeFormatter: {
              month: 'MMM',
              day: 'dd',
              hour: '',
              minute: ''
            }
          }
      }
    };
    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
}

function DailyСharts(click, signup, purchase){
    $("#chart-small-1").html(" ")
    $("#chart-small-2").html(" ")
    $("#chart-small-3").html(" ")

    // Click
    var options1 = {
        chart: {
          height: 100,
          type: "area",
          zoom: {
            enabled: false,
          },
        },
        dataLabels: {
          enabled: false
        },
        series: [
          {
            name: "blue",
            // data: [132, 108, 88, 134, 152]
            data: click
          }
        ],
        colors: ["#470089"],
        fill: {
            colors: ["#470089"],
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 90, 100]
          }
        },
        xaxis: {
          categories: [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
          ]
        }
    };

    var chart1 = new ApexCharts(document.querySelector("#chart-small-1"), options1);

    chart1.render();

// Sing Up
    var options2 = {
        chart: {
          zoom: {
            enabled: false,
          },
          height: 100,
          type: "area"
        },
        dataLabels: {
          enabled: false
        },
        series: [
          {
            name: "red",
            // data: [132, 78, 88, 30, 102]
            data: signup
          }
        ],
        colors: ["#dd2866"],
        fill: {
            colors: ["#dd2866"],
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 90, 100]
          }
        },
        xaxis: {
          categories: [
            "",
            "",
            "",
            "",
            ""
          ]
        }
      };

    var chart2 = new ApexCharts(document.querySelector("#chart-small-2"), options2);

    chart2.render();

// Purchase
    var options3 = {
        chart: {
          zoom: {
            enabled: false,
          },
          height: 100,
          type: "area"
        },
        dataLabels: {
          enabled: false
        },
        series: [
          {
            name: "yellow",
            // data: [132, 78, 88, 100, 152]
            data: purchase
          }
        ],
        colors: ["#ff9900"],
        fill: {
            colors: ["#ff9900"],
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: .9,
            stops: [0, 90, 100]
          }
        },
        xaxis: {
          categories: [
            "",
            "",
            "",
            "",
            ""
          ]
        }
      };

    var chart3 = new ApexCharts(document.querySelector("#chart-small-3"), options3);

    chart3.render();    
}

function SubscriptionCharts(){
    $(function() {
        $('.chart').easyPieChart({
	        barColor: function(percent) {
			    var ctx = this.renderer.getCtx();
			    var canvas = this.renderer.getCanvas();
			    var gradient = ctx.createLinearGradient(0,0,canvas.width,0);
			        gradient.addColorStop(0, "#4dc4e2");
			        gradient.addColorStop(1, "#511d95");
			    return gradient;
			  },
			  scaleColor: false,
			  trackColor: '#dadbda',
			  lineWidth: 6,
			  lineCap: 'round',
			  size: 85
	    });
	});

	$(function() {
        $('.blue-chart').easyPieChart({
	        barColor: function(percent) {
			    var ctx = this.renderer.getCtx();
			    var canvas = this.renderer.getCanvas();
			    var gradient = ctx.createLinearGradient(0,0,canvas.width,0);
			        gradient.addColorStop(0, "#333399");
			        gradient.addColorStop(1, "#bfbfdd");
			    return gradient;
			  },
			  scaleColor: false,
			  trackColor: '#dadbda',
			  lineWidth: chartWidth,
			  lineCap: 'round',
			  size: chartTwoSize
	    });
	});

	$(function() {
        $('.orange-chart').easyPieChart({
	        barColor: function(percent) {
			    var ctx = this.renderer.getCtx();
			    var canvas = this.renderer.getCanvas();
			    var gradient = ctx.createLinearGradient(0,0,canvas.width,0);
			        gradient.addColorStop(0, "#ff9900");
			        gradient.addColorStop(1, "#f0ddc1");
			    return gradient;
			  },
			  scaleColor: false,
			  trackColor: '#dadbda',
			  lineWidth: chartWidth,
			  lineCap: 'round',
			  size: chartTwoSize
	    });
	});

	let chartTwoSize = 115;
	let chartWidth = 9;


	var displayWidth = document.body.clientWidth;
	    if (displayWidth < 580) {
	    	chartTwoSize = 80;
	    	chartWidth = 6;
	    }

	    $(function() {
        $('.red-chart').easyPieChart({
	        barColor: function(percent) {
			    var ctx = this.renderer.getCtx();
			    var canvas = this.renderer.getCanvas();
			    var gradient = ctx.createLinearGradient(0,0,canvas.width,0);
			        gradient.addColorStop(0, "#ed1e6b");
			        gradient.addColorStop(1, "#f9c2d8");
			    return gradient;
			  },
			  scaleColor: false,
			  trackColor: '#dadbda',
			  lineWidth: chartWidth,
			  lineCap: 'round',
			  size: chartTwoSize
	    });
	});
}

function responseSort(response){
  clicks = []
  signups= []
  purchases= []
  days = []

  for(date in response["data"]["date"]){
    clicks.push(response["data"]["date"][date]["clicks"])
    signups.push(response["data"]["date"][date]["signups"])
    purchases.push(response["data"]["date"][date]["purchases"])
    days.push(date)
  }

  return {
    "clicks": clicks,
    "signups": signups,
    "purchases": purchases,
    "days": days
  }
}

function showTotalData(total_data, total_devices){
  TotalСharts(total_data)
  SubscriptionCharts()

  $(".desktop__users").html(total_devices["pc"])
  $(".tablet__users").html(total_devices["mobile"])
  $(".mobile__users").html(total_devices["tablet"])
}

function TotalСharts(total_data){
  var total_click = total_data["clicks"]
  var total_signup = total_data["signups"]
  var total_purchase = total_data["purchases"]

  if(total_click == 0){
    var click_percent = 0
  }else{
    var click_percent = 90
  }
  var signup_percent = (click_percent / total_click) * total_signup
  var purchase_percent = (click_percent / total_click) * total_purchase

  $(".blue-chart").attr('data-percent', click_percent)
  $(".red-chart").attr('data-percent', signup_percent)
  $(".orange-chart").attr('data-percent', purchase_percent)

  $(".blue-chart span").html(total_click)
  $(".red-chart span").html(total_signup)
  $(".orange-chart span").html(total_purchase) 
}

function DayStatsData(day_data){
  DailyСharts(day_data["chart"]["click"], day_data["chart"]["signup"], day_data["chart"]["purchase"])

  $(".chart-small-text:eq(0) span").html(day_data["total"]["click"])
  $(".chart-small-text:eq(1) span").html(day_data["total"]["signup"])
  $(".chart-small-text:eq(2) span").html(day_data["total"]["purchase"])

  $(".profile__traffic-content").html(" ")
  if(day_data["day_stats"].length == 0){
    $(".profile__traffic-content").append("<h3 class='not-found-trafic'>There is currently no traffic. To attract traffic, we recommend advertising your link through Facebook ads, Google ads, YouTube, Twitter</h3>")
    return false
  }
  
  for(i = 0; i < day_data["day_stats"].length; i++){
    var ip = day_data["day_stats"][i]["ip"]
    var device = day_data["day_stats"][i]["device"]
    var country = day_data["day_stats"][i]["country"]
    var city = day_data["day_stats"][i]["city"]
    var time = day_data["day_stats"][i]["time"]
    var type = day_data["day_stats"][i]["type"]
  
    var usd = "0 USD"
    if(type == "purchase"){
      // console.log((day_data["day_stats"][i]["amout"]).toString())
      usd = (day_data["day_stats"][i]["amout"]).toString() + " USD"
    }


    var money_class = ""
    if(type == "click"){
      var div_class = "traffic-purple"
      var span_class = "purple-circle"
    }else if(type == "signup"){
      var div_class = "traffic-red"
      var span_class = "red-circle"
    }else{
      var div_class = "traffic-yellow"
      var span_class = "yellow-circle"
      money_class = "traffic__money-plus"
    }
  
    if(device == "pc"){
      var icon = "<i class='fas fa-desktop device_icon'></i>"
    }else if(device == "mobile"){
      var icon = "<i class='fas fa-mobile-alt device_icon'></i>"
    }else{
      var icon = "<i class='fas fa-tablet-alt device_icon'></i>"
    }
  
    
    var block = "<div class='" + div_class + "'><div class='traffic-text'><span class='circle " + span_class + "'>" + ip + "</span>" + icon + "<i class='trafic-item-time'>| " + time +"</i>" + "<p>" + country + ", " + city + "</p></div><div class='traffic-money " + money_class + "'>" + usd + "</div></div>"
    

    $(".profile__traffic-content").append(block)
    
  }
}

function createLoader(parent_el){
  parent_el.append('<div class="loader_background"><section><div class="sk-fading-circle"><div class="sk-circle sk-circle-1"></div><div class="sk-circle sk-circle-2"></div><div class="sk-circle sk-circle-3"></div><div class="sk-circle sk-circle-4"></div><div class="sk-circle sk-circle-5"></div><div class="sk-circle sk-circle-6"></div><div class="sk-circle sk-circle-7"></div><div class="sk-circle sk-circle-8"></div><div class="sk-circle sk-circle-9"></div><div class="sk-circle sk-circle-10"></div><div class="sk-circle sk-circle-11"></div><div class="sk-circle sk-circle-12"></div></div></section></div>');  
}

