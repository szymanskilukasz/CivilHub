//
// idea-create.js
// ==============
// 
// Formularz do tworzenia/edycji idei.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'jqueryui',
           'redactor',
           'js/modules/common',
           'js/modules/editor/plugins/uploader',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/ideas/idea-form',
           'js/modules/ideas/category-creator'],

  function ($) {
      
    "use strict";
    
    $(document).trigger('load');
      
  });
});