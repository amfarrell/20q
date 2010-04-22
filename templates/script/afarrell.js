$(document).ready(function(){
   $("a").click(function(event){
     alert("Thanks for visiting!");
});
   $("#question").html("red");
});

function sendJson(){
    $.post("test/answerQuestion",{answer: "yes"})
}
