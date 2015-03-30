define([
	"dojo/_base/declare",
	"dojo/_base/fx",
	"dojo/_base/lang",
	"dojo/_base/array",
	"dojo/dom-construct",
	"dojo/dom",
	"dojo/on",
	"dojo/query",
	"dojo/text!./templates/template_guestbook.html",
	"dijit/form/ValidationTextBox",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dijit/_WidgetsInTemplateMixin",
	"dijit/registry",
	"myApp/view/Greeting",
	"myApp/GuestbookStoreRest",
], function(declare, baseFx, lang, array, domConstruct,dom, on, query, template, ValidationTextBox,
			_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin, registry, Greeting, GuestbookStoreRest){

		return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

			templateString: template,
			guestbookStore: null,
			guestbookName: "",

			constructor: function(data){
				this.guestbookName = data.guestbook_name;
				this.guestbookStore = new GuestbookStoreRest(this.guestbookName);
			},

			postCreate: function(data){
				this.inherited(arguments);
				this.textSwitchGuestbookNode.set("value", this.guestbookName);
				this.getGreetings();

				this.own(
					on(this.submitSwitchGuestbookNode,
						"click", lang.hitch(this, "changeGuestBook")),
					on(this.submitNewGreetingNode,
						"click", lang.hitch(this, "addNewGreeting"))
				);
			},

			changeGuestBook: function(){
				console.log(this.textSwitchGuestbookNode);
				this.guestbookName = this.textSwitchGuestbookNode.get("value");
				this.getGreetings();
			},

			getGreetings: function(){
				array.forEach(query(".widget_greeting"), function(greetingNode){
					var widget = registry.byNode(greetingNode);
					widget.destroy();
				})

				this.guestbookStore.getGreetings(this.guestbookName, "")
					.then(lang.hitch(this, function(result){
						var greetings = result.greetings;
						var docFragment = document.createDocumentFragment();
						console.log(docFragment)
						array.forEach(greetings, lang.hitch(this, function(greeting){
								var data = {
									"guestbook_store": this.guestbookStore,
									"guestbook_name": result.guestbook_name,
									"greeting_id": greeting.greeting_id,
									"updated_by": greeting.greeting_auth,
									"content": greeting.greeting_content,
									"date": greeting.greeting_date
								}
								var greeting = new Greeting(data);
								greeting.startup();
								console.log(greeting.domNode)
								docFragment.appendChild(greeting.domNode);
							})
						);
						console.log(docFragment)
						domConstruct.place(docFragment, "greetings", "before");
					}), function(error){
						alert(error);
					});
			},

			addNewGreeting: function(){
				if (this.textNewGreetingNode.validate() == true) {
					this.guestbookStore.addGreeting(this.guestbookName,
						this.textNewGreetingNode.get("value")).then(lang.hitch(this, function (data) {
							alert("Insert Success");
							this.textNewGreetingNode.set("value", "");
							this.getGreetings();
						}), function (error) {
							alert(error);
						}
					)
				}else{
					alert("Form invalid");
				}
			}
		});
});