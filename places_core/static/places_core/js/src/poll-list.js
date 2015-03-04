//
// poll-list.js
// ============
// 
// Lista wszystkich ankiet utworzonych w ramach jednej lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/ui',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/polls/poll-list/pollList',
           'js/modules/inviter/userinviter'],

  function ($) {

    "use strict";

    $(document).trigger('load');
      
  });
});