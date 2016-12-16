var CCOUNT;
$(document).ready(function () {
    $('#btnct').click(function () {
        CCOUNT = $('#seconds').val();
        CCOUNT=CCOUNT*60
        cdreset();
    });
});
var t, count;


function cddisplay() {
    document.getElementById('hspan').innerHTML = Math.floor(count/3600);
    document.getElementById('minspan').innerHTML = Math.floor((count-Math.floor(count/3600)*3600)/60);
    document.getElementById('secspan').innerHTML =  count%60;

}

function countdown() {
    // starts countdown
    cddisplay();
    if (count === 0) {

    } else {
        count--;
        t = setTimeout(countdown, 1000);
    }

}

function cdpause() {
    // pauses countdown
    clearTimeout(t);
}

function cdreset() {
    // resets countdown
    cdpause();
    count = CCOUNT;
    cddisplay();
}/**
 * Created by abedi on 12/16/2016.
 */
