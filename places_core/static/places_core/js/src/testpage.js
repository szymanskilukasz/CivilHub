//
// testpage.js
// ===========

// Te skrypty nie mają zastosowania na żadnej podstronie.
// Są tylko do testowania różnego stuffu.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common'],
           
  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
