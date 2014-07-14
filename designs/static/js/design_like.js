function toggle_like() {
	//loading();
	url = document.URL.split('designs/')[1].split('/')[0]
	Dajaxice.designs.toggle_like(Dajax.process,{'design_url':url});
}

function show_unlike() {
	$('.like_button').removeClass('liked');
	$('.like_button').addClass('unliked');
	$('.like_hint').css('visibility', 'visible')

	//update like nr
	likes = parseInt($('#like_nr').html())
	$('#like_nr').html(likes - 1);

	//update like percentage
	perc = (likes - 1) * 100/110;
	$('#like_perc').html(perc.toFixed(0) + '%');
	$('#prog_bar').width(perc + '%');
}

function show_like() {
	$('.like_button').removeClass('unliked');
	$('.like_button').addClass('liked');
	$('.like_hint').css('visibility', 'hidden')

	//update like nr
	likes = parseInt($('#like_nr').html())
	$('#like_nr').html(likes + 1);

	//update like percentage
	perc = (likes + 1) * 100/110;
	$('#like_perc').html(perc.toFixed(0) + '%');
	$('#prog_bar').width(perc + '%');

	//show like on facebook
	Dajaxice.designs.fb_like(Dajax.process,{'design_url':url});
}

function resubmit() {
	//remove link
	$('#resubmit_txt').attr('onclick', '')
	$('#resubmit_txt').html('Thanks!')
	url = document.URL.split('designs/')[1].split('/')[0]
	Dajaxice.designs.resubmit(Dajax.process,{'design_url':url});
}