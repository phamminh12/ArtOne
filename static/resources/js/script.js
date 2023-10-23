$(document).ready(
    function () {

        // sticky nav
        $('.about-section').waypoint(
            function (direction) {
                if (direction == "down") {
                    $('nav').addClass('sticky');
                } else {
                    $('nav').removeClass('sticky');
                }
            }, {
            offset: '600px'
        }
        )

        // scroll
        $('a').click(function (event) {
            $('html, body').animate({
                scrollTop: $($.attr(this, 'href')).offset().top
            }, 500);
            event.preventDefault();
        });

        // mobile navigation
        $('.mobile-nav-icon').click(
            function () {
                $('.main-nav').slideToggle(200);

                if ($('.mobile-nav-icon').hasClass('fa-bars')) {
                    $('.mobile-nav-icon').addClass('fa-xmark');
                    $('.mobile-nav-icon').removeClass('fa-bars');
                }
                else {
                    $('.mobile-nav-icon').addClass('fa-bars');
                    $('.mobile-nav-icon').removeClass('fa-xmark');
                }
            }
        )

        // lỗi khi click vào .login hiện ra .dropdow nhưng tự động đóng lại luôn
        // $('.login').click(
        //     function() 
        //         {
        //             $('.dropdow').slideToggle(200);
        //         }
        // )
        $(document).ready(function () {
            let isDropdownVisible = false;
            let clickCount = 0;
            $('.login').click(function () {
                clickCount++;
                setTimeout(function () {
                    clickCount--;
                    if (clickCount === 0) {
                        if (isDropdownVisible) {
                            $('.dropdow').slideUp(200);
                            isDropdownVisible = false;
                        } else {
                            $('.dropdow').slideDown(200);
                            isDropdownVisible = true;
                        }
                    }
                }, 200);
            });
            $(document).click(function (event) {
                if (!$(event.target).closest('.login, .dropdow').length) {
                    $('.dropdow').slideUp(200);
                    isDropdownVisible = false;
                    clickCount = 0;
                }
            });
        });


        $('.dropdown-blog').click(
            function () {
                $('.dropdown--menu').slideToggle(200);
            }
        )

    }
)
