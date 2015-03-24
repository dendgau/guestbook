define([
    "dojo/_base/declare",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
	"dojo/text!./templates/template_greeting.html",
    "myApp/GuestbookStore",
	"dojo/_base/fx",
	"dojo/_base/lang",
    "dijit/form/Button"
], function(declare, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,template, _GuestbookStore, baseFx, lang, button){

        return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

            templateString: template,
            baseClass: "widget_greeting",
            guestbook_name: "",
            greeting_id: "",
            author: "",
            content: "",
            date: "",

            constructor: function(data){
                this.guestbook_name = data.guestbook_name;
                this.greeting_id = data.greeting_id;
                this.content = data.content;
                this.date = data.date;
                if (data.updated_by !== null){
                    this.author = data.updated_by;
                }else{
                    this.author = "Anonymous Person";
                }
            },

            postCreate: function(data){
                this.inherited(arguments);
            },

            delete: function(){
                _GuestbookStore.access_api_delete_greeting(this.guestbook_name, this.greeting_id).then(function(data){
                    alert(data);
                }, function(err){
                    alert(err);
                });
                this.destroyRecursive();
            }
        });
});