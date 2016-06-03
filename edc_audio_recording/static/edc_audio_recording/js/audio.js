function startPlayback(pk, url) {
	play = '#play-' + pk
	stop = '#stop-' + pk
	$.ajax({
		type:'GET',
		url: url,
		data:{
			action:"play",
		},
		success:function(json){
			$(stop).show();
			$(play).show();
		},
	});
	return true;
}

function stopPlayback(pk, url) {
	play = '#play-' + pk
	stop = '#stop-' + pk
	$.ajax({
		type:'GET',
		url: url,
		data:{
			action:"stop",
		},
		success:function(json){
			$(stop).show();
			$(play).show();
		},
	});
	return true;
}

function startRecording(e){
	e.preventDefault();
	$('#alert-saving').hide();
	$('#alert-saved').hide();
	$.ajax({
		type:'GET',
		url:"{% url 'record' app_label model_name pk %}",
		data:{
			action:"start_recording",
		},
		success:function(json){
			$("#audio-status").text(json.status + ': ' + json.message);
			$("#btn-record").removeClass( "btn-default" ).addClass( "btn-danger" );
			$("#btn-record").text('Recording ...');
			$("#btn-record").prop( "disabled", false );
			$("#btn-stop").prop( "disabled", false );
			$("#btn-cancel").hide();
			$("#li-topbar-home").addClass("disabled");
			$("#li-topbar-settings").addClass("disabled");
			$("#li-topbar-user-profile").addClass("disabled");
			$("#li-topbar-logout").addClass("disabled");
			poll();
		}
	});
}

function stopRecording(e){
	e.preventDefault();
	$("#btn-record").prop( "disabled", true );
	$("#btn-record").text('Saving ...');
	$('#alert-saving').show();
	$.ajax({
		type:'GET',
		url:"{% url 'record' app_label model_name pk %}",
		data:{
			action:"stop_recording",
		},
		success:function(json){
			$("#btn-record").removeClass( "btn-danger" ).addClass( "btn-default" );
			$("#btn-record").prop( "disabled", true );
			$("#btn-record").text('Click to Record');
			$("#btn-stop").prop( "disabled", true );
			$('#alert-saving').hide();
			$('#alert-saved').show();
			$("#li-topbar-home").removeClass("disabled");
			$("#li-topbar-settings").removeClass("disabled");
			$("#li-topbar-user-profile").removeClass("disabled");
			$("#li-topbar-logout").removeClass("disabled");
		}
	});
}


function poll() {
    $.ajax({
        url: "{% url 'record' app_label model_name pk %}",
        type: "GET",
        success: function(json) {
			action:"duration";
            if(json.status == 'recording') {
        		setTimeout(function() {poll()}, 1000);
        		$("#audio-duration").text(json.recording_time);
        	};
        },
        dataType: "json",
        timeout: 900
    });
}
