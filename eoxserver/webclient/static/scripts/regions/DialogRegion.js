(function(){"use strict";var a=this;a.define(["backbone","communicator","backbone.marionette"],function(a,b){var c=a.Marionette.Region.extend({constructor:function(){_.bindAll(this),a.Marionette.Region.prototype.constructor.apply(this,arguments),this.on("show",this.showModal,this)},getEl:function(a){var b=$(a);return b.on("hidden",this.close),b},showModal:function(a){a.on("close",this.hideModal,this),a.$el.modal("show")},hideModal:function(){}});return c})}).call(this);