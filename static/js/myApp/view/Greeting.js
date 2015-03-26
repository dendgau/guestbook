define([
    "dojo/_base/declare",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dojo/text!./templates/template_greeting.html",
    "myApp/GuestbookStore",
	"dojo/_base/fx",
	"dojo/_base/lang",
    "dojo/query",
    "dojo/dom-style",
    "dojo/dom",
    "dojo",
    "dijit/registry",
    "dijit/form/Button",
    "dijit/form/Form",
    "dijit/form/TextBox",
    "dijit/form/Textarea",
    "dijit/_WidgetsInTemplateMixin",
], function(declare, _WidgetBase, _TemplatedMixin, template, _GuestbookStore, baseFx,
            lang, query, domStyle, dom, dojo, registry, button, _form, _textbox, _textarea,
            _WidgetsInTemplateMixin){

        return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

            templateString: template,

            _guestbook_store: null,
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
                this._guestbook_store = data.guestbook_store;
                console.log(data.guestbook_store);
            },

            postCreate: function(data){
                this.inherited(arguments);
            },

            delete: function(){
                this._guestbook_store.access_api_delete_greeting(this.guestbook_name, this.greeting_id)
                    .then(function(data){
                    alert("Delete Success");
                }, function(err){
                    alert(err);
                });
                this.destroyRecursive();
            },

            _edit_greeting_event: function(){
                var me = this;
                this._guestbook_store.access_api_get_greeting_detail(
                    this.guestbook_name, this.greeting_id
                ).then(function(data){
                    var formNode = me.editFormNode;
                    domStyle.set(formNode, {"display": "block"});
                    me.edit_greeting_content.innerHTML = data.content;
                }, function(error){
                    alert(error);
                })
            },

            _update_greeting: function(){
                this.content = this.edit_greeting_content.value
                var me = this;
                this._guestbook_store.access_api_put_greeting(
                    this.guestbook_name, this.greeting_id, this.content
                ).then(function(data){
                    alert("Update Success");
                    me.contentNode.innerHTML = me.content
                    var formNode = me.editFormNode;
                    domStyle.set(formNode, {"display": "none"});
                }, function(error){
                    alert(error);
                })
            }
        });
});