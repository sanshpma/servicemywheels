$(function(){

    var contentInitialOffset = $('.mainContentFooterArea').offset().top ;


    $(window).scroll(function() {
        if($(window).scrollTop()-$('.sideBar').offset().top >= 0){
            $('.sideBar').addClass('fixedSideBar');
        }
        if($(window).scrollTop() <= contentInitialOffset){
            $('.sideBar').removeClass('fixedSideBar');
        }
    });

    $('#resizeSideBar').click(function(){
        if($('.sideBar').hasClass('resizedSideBar')){
            $('.sideBarNav li a .textSpan').toggle('slow');
        }
        else{
            $('.sideBarNav li a .textSpan').toggle('fast');
        }
        $('.resizeCollapseImage').toggleClass('hidden');
        $('.resizeExpandImage').toggleClass('hidden');
        $('.sideBar').toggleClass("resizedSideBar",'slow');
        $('.mainContentFooterArea').toggleClass("resizedMainContentArea",'slow');
        return false;
    });

    $('#showDropDownLink').click(function(){
        $('.accSettLogoutDiv').toggle();
        return false;
    });
    $('html, body').click(function(){
        $('.accSettLogoutDiv').hide();
    });


    $('#codeSettingsEditLink').click(function(){
        $('html, body').animate({
            scrollTop:0
        }, 'slow');
        $('.popUpWrapper').fadeIn('fast');
        $('#editCodeSettingsPopup').fadeIn('fast');
        return false;
    });
    $('#editAccSettingsLink').click(function(){
        $('html, body').animate({
            scrollTop:0
        }, 'slow');
        $('.popUpWrapper').fadeIn('fast');
        $('#editAccSettingsPopup').fadeIn('fast');
        return false;
    });

});