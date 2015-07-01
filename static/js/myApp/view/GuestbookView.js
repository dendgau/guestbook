define([
	"dojo/_base/declare",
	"dojo/_base/fx",
	"dojo/_base/lang",
	"dojo/_base/array",
	"dojo/dom-construct",
	"dojo/dom",
	"dojo/on",
	"dojo/query",
	"dojo/text!./templates/GuestbookView.html",
	"dijit/form/ValidationTextBox",
	"dijit/form/Button",
	"dijit/registry",
	"myApp/view/GreetingView",
	"myApp/GuestbookStore",
	"myApp/view/_ViewBaseMixin"
], function(declare, baseFx, lang, array, domConstruct,dom, on, query, template, ValidationTextBox,
			_WidgetsInTemplateMixin, registry, GreetingView, GuestbookStore, _ViewBaseMixin){

		return declare([_ViewBaseMixin], {

			templateString: template,
			guestbookStore: null,
			guestbookName: "",

			constructor: function(data){
				this.guestbookName = data.guestbook_name;
				this.guestbookStore = new GuestbookStore();
				this.guestbookStore.set("guestbookName", this.guestbookName);
			},

			postCreate: function(data){
				this.inherited(arguments);
				this.refreshGreetings();

				this.own(
					on(this.switchGuestbookButton,
						"click", lang.hitch(this, "changeGuestBook")),
					on(this.submitNewGreetingButton,
						"click", lang.hitch(this, "addNewGreeting"))
				);
			},

			changeGuestBook: function(){
				this.guestbookName = this.textSwitchGuestbook.get("value");
				this.refreshGreetings();
			},

			clearGreetings: function(){
				array.forEach(query(".widgetGreeting"), function(greetingNode){
					var widget = registry.byNode(greetingNode);
					widget.destroy();
				})
			},

			getGreetings: function(){
				this.guestbookStore.set("guestbookName", this.guestbookName);
				this.guestbookStore.getGreetings("")
					.then(lang.hitch(this, function(result){
						var greetings = result.greetings;
						var docFragment = document.createDocumentFragment();
						var arrayWidgetGreeting = [];
						array.forEach(greetings, lang.hitch(this, function(greeting){
								var data = {
									"guestbook_store": this.guestbookStore,
									"guestbook_name": result.guestbook_name,
									"greeting_id": greeting.greeting_id,
									"updated_by": greeting.greeting_auth,
									"content": greeting.greeting_content,
									"date": greeting.greeting_date
								}
								var greeting = new GreetingView(data);
								docFragment.appendChild(greeting.domNode);
								arrayWidgetGreeting.push(greeting);
							})
						);
						domConstruct.place(docFragment, "greetings", "before");
						array.forEach(arrayWidgetGreeting, lang.hitch(this, function(greeting){
								greeting.startup();
							})
						);
					}), function(error){
					});
			},

			refreshGreetings: function(){
				this.clearGreetings();
				this.getGreetings();
			},

			addNewGreeting: function(){
				if (this.textNewGreeting.validate() == true) {
					var messageGreeting = this.textNewGreeting.get("value");
					this.guestbookStore.set("guestbookName", this.guestbookName);
					this.guestbookStore.addGreeting(messageGreeting)
						.then(lang.hitch(this, function (data) {
							alert("Insert Success");
							this.textNewGreeting.set("value", "");
							this.refreshGreetings();
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