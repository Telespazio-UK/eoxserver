(function(){"use strict";var a=this;a.define(["backbone","communicator","hbs!tmpl/LayerControl","underscore"],function(a,b,c){var d=a.Marionette.Layout.extend({template:{type:"handlebars",template:c},regions:{baseLayers:"#baseLayers",products:"#products",overlays:"#overlays"},className:"panel panel-default layercontrol not-selectable",events:{},initialize:function(){},onShow:function(){this.$(".close").on("click",_.bind(this.onClose,this)),this.$el.draggable({handle:".panel-heading",containment:"#content",scroll:!1,start:function(){$(".ui-slider").detach(),$(".fa-adjust").toggleClass("active"),$(".fa-adjust").popover("hide")}})},onClose:function(){this.close()}});return d})}).call(this);