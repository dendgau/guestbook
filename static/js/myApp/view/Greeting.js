define([
    "dojo/_base/declare",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
	"dojo/text!./templates/template_greeting.html",
	"dojo/_base/fx",
	"dojo/_base/lang"
], function(declare, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,template, baseFx, lang){

        return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

            templateString: template,
            greeting_id: "a",
            updated_by: "a",
            content: "a",
            date: "a",

            constructor: function(data){
                this.greeting_id = data.greeting_id;
                this.updated_by = data.updated_by;
                this.content = data.content;
                this.date = data.date;
            },

            postCreate: function(data){
                this.inherited(arguments);
            },

            delete: function(){
                this.destroyRecursive();
            }

        });
});