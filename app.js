$(document).ready(function() {
  $('.flashcard').on('click', function() {
    $('.flashcard').toggleClass('flipped');
  });
});

$(document).keydown(function(e){
    if (e.which == 39){
        if ($("#next").attr('href'))
            window.location.href = window.location.href.substring(0, window.location.href.lastIndexOf("/")) + "/" + $("#next").attr('href');
    }
    else if (e.which == 37){
        if ($("#previous").attr('href'))
            window.location.href = window.location.href.substring(0, window.location.href.lastIndexOf("/")) + "/" + $("#previous").attr('href');
    }
    else if (e.which == 32 || e.which == 13){
        $('.flashcard').toggleClass('flipped');
    }
    else if (e.which == 8 || e.which == 46){
        window.location.href = window.location.href.substring(0, window.location.href.lastIndexOf("/")) + "/" + $("#restart").attr('href');
    }
    else if (e.which == 27){
        if ($("#index").attr('href'))
            window.location.href = $("#index").attr('href');
        else
            window.location.href = "index.html";
    }
});