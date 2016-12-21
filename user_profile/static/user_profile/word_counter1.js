counter = function() {
    var value = $('#id_text').val();

    if (value.length == 0) {
        $('#wordCount').html(0);

        return;
    }

    var regex = /\s+/gi;
    var wordCount = value.trim().replace(regex, ' ').split(' ').length;


    $('#wordCount').html(wordCount);
console.log(wordCount)
};

$(document).ready(function() {
    $('#id_text').click(counter);
    $('#id_text').change(counter);
    $('#id_text').keydown(counter);
    $('#id_text').keypress(counter);
    $('#id_text').keyup(counter);
    $('#id_text').blur(counter);
    $('#id-text').focus(counter);
});/**
 * Created by abedi on 12/21/2016.
 */
