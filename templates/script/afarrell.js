$(document).ready(function(){
    $("input[value='True']").click(function(event){
        // Select the input whose value equals true
        // when it is clicked, call a function
        // that we have declared right here
        sendAnswer('True');
    });
    $("input[value='False']").click(function(event){
        sendAnswer('False');
    });
});

function changequestion(text){
    $("#question").html(text);
    // set the text of the question to whatever the text this function
    // recieves is.
}
function sendAnswer(text){
    $.post("/test/answerQuestion",{'userAnswer':text},changequestion);
    // post the text to the server
    // when we get a response,
    // call changequestion
}
