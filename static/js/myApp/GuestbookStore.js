define([
	"dojo/_base/declare",
	"dojo/store/JsonRest",
	"dojo/cookie",
	"dojo/Stateful"
], function(declare, JsonRest, cookie, Stateful){
	return declare([Stateful],{
		jsonRest: null,
		guestbookName: null,

		_guestbookNameGetter: function(){
			return this.guestbookName;
		},

		_guestbookNameSetter: function(guestbook_name){
			this.guestbookName = guestbook_name;
		},

		constructor: function(){
			this.watch("guestbookName", function(name, oldValue, value){
				if (oldValue !== value){
					this.guestbookName = value;
					this.jsonRest = new JsonRest({
						target: "/guestbook_app/api/guestbook/" + this.guestbookName + "/greeting",
						headers: {"X-CSRFToken": cookie("csrftoken")}
					});
				}
			});
		},

		getGreetings: function(guestbook_name, cursor){
			console.log(this.jsonRest)
			return this.jsonRest.query({
				"cursor" : cursor
			});
		},

		addGreeting: function(greeting_message){
			return this.jsonRest.add({
				"greeting_message": greeting_message
			});
		},

		deleteGreeting: function(greeting_id){
			return this.jsonRest.remove(greeting_id);
		},

		getGreetingDetail: function(greeting_id){
			return this.jsonRest.get(greeting_id);
		},

		updateGreeting: function(greeting_id, greeting_message){
			return this.jsonRest.put({
				"greeting_message": greeting_message,
				"id": greeting_id
			});
		}
	});
});
