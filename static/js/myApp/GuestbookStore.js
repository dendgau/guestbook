define([
	"dojo/_base/declare",
	"dojo/Deferred",
	"dojo/store/Memory",
	"dojo/store/JsonRest",
	"dojo/store/Cache",
	"dojo/cookie",
], function(declare, Deferred, Memory, JsonRest, Cache, cookie){
	return declare([],{
		jsonRest: null,
		guestbookName: "",

		constructor: function(guestbook_name){
			this.guestbookName = guestbook_name;
			this.jsonRest = new JsonRest({
				target: "/guestbook_app/guestbook/" + this.guestbookName + "/greeting",
				headers: {"X-CSRFToken": cookie("csrftoken")}
			});
		},

		checkTargetChange: function(guestbook_name){
			if (this.guestbookName !== guestbook_name){
				this.guestbookName = guestbook_name;
				this.jsonRest = new JsonRest({
					target: "/guestbook_app/guestbook/" + this.guestbookName + "/greeting",
					headers: {"X-CSRFToken": cookie("csrftoken")}
				});
			}
		},

		getGreetings: function(guestbook_name, cursor){
			this.checkTargetChange(guestbook_name);
			return this.jsonRest.query({
				"cursor" : cursor
			});
		},

		addGreeting: function(guestbook_name, greeting_message){
		   this.checkTargetChange(guestbook_name);
			return this.jsonRest.add({
				"guestbook_name": guestbook_name,
				"greeting_message": greeting_message
			});
		},

		deleteGreeting: function(guestbook_name, greeting_id){
			this.checkTargetChange(guestbook_name);
			return this.jsonRest.remove(greeting_id);
		},

		getGreetingDetail: function(guestbook_name, greeting_id){
			this.checkTargetChange(guestbook_name);
			console.log(this.jsonRest.get(greeting_id))
			return this.jsonRest.get(greeting_id);
		},

		updateGreeting: function(guestbook_name, greeting_id, greeting_message){
			this.checkTargetChange(guestbook_name);
			return this.jsonRest.put({
				"guestbook_name": guestbook_name,
				"greeting_message": greeting_message,
				"id": greeting_id
			});
		}
	});
});
