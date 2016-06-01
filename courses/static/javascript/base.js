$(window).load(function()
{

    $(".loading-overlay .sk-folding-cube").fadeOut(1000,
        function()
        {
            $(this).parent().fadeOut(1000,function(){
                $("body").css("overflow","auto");
               $(this).remove();
            });
        });


});

