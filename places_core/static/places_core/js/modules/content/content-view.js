//
// content-view.js
// ===============

// Widok pojedynczego elementu dla paginowalnej
// kolekcji obsługującej filtry i lazy-loader.

define(['underscore', 'backbone'],

function (_, Backbone) {
    
  "use strict";
  
  var ContentView = Backbone.View.extend({
      
    tagName: 'div',
    
    className: 'col-sm-4 locBoxH',
    
    template: _.template($('#content-item-tpl').html()),
    
    render: function () {
      var imgUrl = utils.isRetina() ? this.model.get('retina_thumbnail')
                                    : this.model.get('thumbnail');
      this.$el.html(this.template(this.model.toJSON()));
      this.$('.locBoxIcon').find('a').tooltip();
      this.$('.locBoxHeader:first')
        .css('background-image', "url(" + imgUrl + ")");
      return this;
    }
  });
  
  return ContentView;
});