define([
	"dojo/_base/declare",
	"dojo/_base/fx",
	"dojo/_base/lang",
	"dojo/on",
	"dojo/query",
	"dojo/dom-style",
	"dojo/dom",
	"dojo/text!./templates/template_greeting.html",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dijit/registry",
	"dijit/form/Button",
	"dijit/form/Form",
	"dijit/form/TextBox",
	"dijit/_WidgetsInTemplateMixin",

], function(declare, baseFx, lang, on, query, domStyle, dom, template, _WidgetBase, _TemplatedMixin,
			registry, button, form, textbox, _WidgetsInTemplateMixin, ValidationTextBox){

		return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

			templateString: template,
			baseClass: "widget_greeting",
			guestbookStore: null,
			guestbookName: "",
			greeting_id: "",
			author: "",
			content: "",
			date: "",

			constructor: function(data){
				this.guestbookName = data.guestbook_name;
				this.greeting_id = data.greeting_id;
				this.content = data.content;
				this.date = data.date;
				if (data.updated_by !== "None"){
					this.author = data.updated_by;
				}else{
					this.author = "Anonymous Person";
				}
				this.guestbookStore = data.guestbook_store;
			},

			postCreate: function(data){
				this.inherited(arguments);

				this.own(
					on(this.deleteButtonNode,
						"click", lang.hitch(this, "deleteGreeting")),
					on(this.openEditFormNode,
						"click", lang.hitch(this, "openEditForm")),
					on(this.submitUpdateGreetingNode,
						"click", lang.hitch(this, "updateGreeting"))
				);
			},

			deleteGreeting: function(){
				this.guestbookStore.deleteGreeting(this.guestbookName, this.greeting_id)
					.then(lang.hitch(this, function(data){
						alert("Delete Success");
						this.destroyRecursive();
				}), function(error){
					alert(error);
				});
			},

			openEditForm: function(){
				this.guestbookStore.getGreetingDetail(this.guestbookName, this.greeting_id)
					.then(lang.hitch(this, function(data){
						var formNode = this.editFormNode;
						domStyle.set(formNode, {"display": "block"});
						this.textEditGreetingNode.set("value", data.content);
				}), function(error){
					alert(error);
				});
			},

			updateGreeting: function(){
                if (this.textEditGreetingNode.validate() == true) {
                    this.content = this.textEditGreetingNode.value
                    this.guestbookStore.updateGreeting(
                        this.guestbookName, this.greeting_id, this.content
                    ).then(lang.hitch(this, function () {
                            alert("Update Success");
                            this.contentNode.innerHTML = this.content
                            var formNode = this.editFormNode;
                            domStyle.set(formNode, {"display": "none"});
                        }), function (error) {
                            alert(error);
                        })
                }else{
                    alert("Form Invalid");
                }
			}
		});
});