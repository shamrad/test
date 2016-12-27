/**
 * Created by Shayan on 12/7/2016.
 */
// $(document).ready(function(){
//     // set up hover panels
//     // although this can be done without JavaScript, we've attached these events
//     // because it causes the hover to be triggered when the element is tapped on a touch device
//     $('.hover').hover(function(){
//         $(this).addClass('flip');
//     },function(){
//         $(this).removeClass('flip');
//     });
// });

$('.flip').hover(function(){
    $(this).find('.card').toggleClass('flipped');

});


// typed script
$(function(){

        $("#typed").typed({
            // strings: ["Typed.js is a <strong>jQuery</strong> plugin.", "It <em>types</em> out sentences.", "And then deletes them.", "Try it out!"],
            stringsElement: $('#typed-strings'),
            typeSpeed: 30,
            backDelay: 500,
            loop: false,
            contentType: 'html', // or text
            // defaults to false for infinite loop
            loopCount: false,
            callback: function(){ foo(); },
            resetCallback: function() { newTyped(); }
        });

        $(".reset").click(function(){
            $("#typed").typed('reset');
        });

    });

    function newTyped(){ /* A new typed object */ }

    function foo(){ console.log("Callback"); }

// scroll down script
$(document).ready(function() {
$(".totop").click(function() {
     $('html, body').animate({
         scrollTop: $(".up").offset().top
     }, 1500);
 });
});