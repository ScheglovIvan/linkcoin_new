let burger = document.querySelector(".burger-menu");
let burger2 = document.querySelector(".starter-burger");
let bodyEl = document.getElementById('body');
let menu = document.querySelectorAll(".menu");

let spanOne = document.getElementById("burger-span-one");
let spanTwo = document.getElementById("burger-span-two");
// let headerLogo = document.getElementById("header-logo");

var schet = 0;

$(document).ready(function(){

	$(window).scroll(function() {
		var anim_stop = 650
		if($(window).width() < 860){
			anim_stop = 550
		}else if($(window).width() < 430){
			anim_stop = 400
		}

		if($(this).scrollTop() < anim_stop) {
			$(".anim_off").removeClass("anim_off")
		}else if($(this).scrollTop() >= anim_stop) {
			$(".anim").addClass("anim_off")
		}
	});

	$(".menu").on("click","a", function (event) {
		spanOne.style.background = "rgb(66,0,128)";
		spanTwo.style.background = "rgb(66,0,128)";
		// headerLogo.src = "img/logo2.svg";
		menu[0].style.opacity = "0";
		bodyEl.classList.remove("no-scroll");
		burger.classList.remove("active-burger");
		setTimeout(function() {
			menu[0].style.display = "none";
		}, 100);
	});

	$(".upper-menu").on("click","a", function (event) {
		spanOne.style.background = "rgb(66,0,128)";
		spanTwo.style.background = "rgb(66,0,128)";
		// headerLogo.src = "img/logo2.svg";
		menu[1].style.opacity = "0";
		bodyEl.classList.remove("no-scroll");
		burger.classList.remove("active-burger");
		setTimeout(function() {
			menu[1].style.display = "none";
		}, 100);
	});
});


burger.addEventListener("click", () => {
	schet++;
	if (schet % 2 == 0) {
		spanOne.style.background = "rgb(66,0,128)";
		spanTwo.style.background = "rgb(66,0,128)";
		menu[0].style.opacity = "0";
		bodyEl.classList.remove("no-scroll");
		burger.classList.remove("active-burger");
		setTimeout(function() {
			menu[0].style.display = "none";
		}, 100);
	}

	else {
		spanOne.style.background = "#fff";
		spanTwo.style.background = "#fff";
		menu[0].style.display = "block";
		bodyEl.classList.add("no-scroll");
		burger.classList.add("active-burger");
		setTimeout(function() {
			menu[0].style.opacity = "1";
		}, 100);
	}
});

burger2.addEventListener("click", () => {
	schet++;
	if (schet % 2 == 0) {
		menu[1].style.opacity = "0";
		bodyEl.classList.remove("no-scroll");
		burger2.classList.remove("active-burger");
		setTimeout(function() {
			menu[1].style.display = "none";
		}, 100);
	}

	else {
		menu[1].style.display = "block";
		bodyEl.classList.add("no-scroll");
		burger2.classList.add("active-burger");
		setTimeout(function() {
			menu[1].style.opacity = "1";
		}, 100);
	}
});

function navHeight() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    let navigation = document.querySelector("#header");

    if(scrollTop >= 5) {
    	navigation.style.display = "flex";
    	setTimeout(function() {
    		navigation.style.opacity = "1";
    	},10);
    }

    if(scrollTop < 5) {
    	navigation.style.opacity = "0";
    	setTimeout(function() {
    		navigation.style.display = "none"
    	},10);
    }
}

let leaderBlock = document.querySelector(".leaders__blocks");

function slideCardsRight() {
	leaderBlock.style.transform = "translateX(-70%)";
}

function slideCardsLeft() {
	leaderBlock.style.transform = "translateX(70%)";
}

function slideCardsCenter() {
	leaderBlock.style.transform = "translateX(0%)";
}

 
$(document).ready(function(){
	$("#header").on("click","a", function (event) {
		//отменяем стандартную обработку нажатия по ссылке
		
		//забираем идентификатор бока с атрибута href
		var id  = $(this).attr('href'),

		//узнаем высоту от начала страницы до блока на который ссылается якорь
			top = $(id).offset().top;
		
		//анимируем переход на расстояние - top за 1500 мс
		$('body,html').animate({scrollTop: top}, 1500);
	});

	$(".menu").on("click","a", function (event) {
		//отменяем стандартную обработку нажатия по ссылке
		event.preventDefault();

		//забираем идентификатор бока с атрибута href
		var id  = $(this).attr('href'),

		//узнаем высоту от начала страницы до блока на который ссылается якорь
			top = $(id).offset().top;
		
		//анимируем переход на расстояние - top за 1500 мс
		$('body,html').animate({scrollTop: top}, 1500);
	});

	$(".header-content").on("click","a", function (event) {
		//отменяем стандартную обработку нажатия по ссылке
		event.preventDefault();

		//забираем идентификатор бока с атрибута href
		var id  = $(this).attr('href'),

		//узнаем высоту от начала страницы до блока на который ссылается якорь
			top = $(id).offset().top;
		
		//анимируем переход на расстояние - top за 1500 мс
		$('body,html').animate({scrollTop: top}, 1500);
	});

	$(".pros").on("click","a", function (event) {
		//отменяем стандартную обработку нажатия по ссылке
		event.preventDefault();

		//забираем идентификатор бока с атрибута href
		var id  = $(this).attr('href'),

		//узнаем высоту от начала страницы до блока на который ссылается якорь
			top = $(id).offset().top;
		
		//анимируем переход на расстояние - top за 1500 мс
		$('body,html').animate({scrollTop: top}, 1500);
	});
});
