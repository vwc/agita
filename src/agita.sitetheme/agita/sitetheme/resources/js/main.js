/*global jQuery:false, document:false, window: false */
'use strict';

(function ($) {
  $(document).ready(function () {
    if ($('body').hasClass('lt-ie7')) {return; }
    // Application specific javascript code goes here

    $(document.body).scrollspy({target: '#hero-toc'});
    $(window).on('load', function () {
      $body.scrollspy('refresh');
    });
    setTimeout(function () {
        var $sideBar = $('#hero-toc');
        $sideBar.affix({
            offset: {
              top: function () {
                var offsetTop      = $sideBar.offset().top;
                var sideBarMargin  = parseInt($sideBar.children(0).css('margin-top'), 10);
                var navOuterHeight = $('#hero-toc').height();
                return (this.top = offsetTop - navOuterHeight - sideBarMargin);
              },
              bottom: function () {
                return (this.bottom = $('.bs-docs-footer').outerHeight(true));
              }
            }
      });
    }, 100);

    setTimeout(function () {
      $('.hero-top').affix()
    }, 100);
  });
}(jQuery));
