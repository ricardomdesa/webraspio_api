
$(document).ready(function(){
    console.log('app.js running');

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number " + msg.cont);
        var decremento = msg.tempo - msg.cont;
	var dec_min = decremento / 60;
	
	if(dec_min > 1){
            numbers_string = '<p>' + 'Tempo restante para desligar: ' + 'testeRMS' + '</p>'
	}else{
            //numbers_string = '<p>' + 'Tempo restante para desligar: ' + decremento.toString() + '</p>'
            numbers_string = '<p>' + 'Tempo restante para desligar: ' + 'teste' + '</p>'
	}
        $('#log').html(numbers_string);

        if(msg.cont == 0){
            console.log("atualiza pag")
            window.location.href = 'http://' + document.domain + ':' + location.port + '/';
        }
    });

});
