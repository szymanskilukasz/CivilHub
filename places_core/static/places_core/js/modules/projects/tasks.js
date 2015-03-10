//
// tasks.js
// ========

// Skrypt obsługujący formularz podsumowania projektu.

require(['jquery',
         'js/modules/ui/ui'],

function ($, ui) {
  "use strict";

  function toggleTask (e) {
    var $this = $(e.currentTarget);
    var $form = $this.parent('form');
    $.post($form.attr('action'), {},
      function (response) {
        ui.message.success(response.message);
      }
    )
  }

  $(document).ready(function () {
    $('.fake-submit').hide();
    $('[name="checkbox-task"]').on('click', toggleTask);
  }); 
});