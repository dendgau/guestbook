define([
    "dojo/_base/declare",
    "dojo/store/Memory",
    "dojo/store/JsonRest",
    "dojo/store/Cache",
    "dojo/cookie",
    'dojo/Stateful'
], function(declare, _Memory, _JsonRest, _Cache, cookie){
    return declare([],{
        _store: null,
        guestbookName: "",

        constructor: function(){
            this.watch("guestbookName", function(name, oldValue, newValue){
                if (oldValue !== newValue) {
                    var memoryStore = new _Memory();
                    var jsonRestStore = new _JsonRest({
                        target: "/guestbook_app/guestbook/" + newValue + "/greeting",
                        headers: {"X-CSRFToken": cookie("csrftoken")}
                    });
                    this._store = new _Cache(jsonRestStore, memoryStore);
                }
            })
        },

        access_api_get_list_greeting: function(guestbook_name, cursor){
            this.guestbookName = guestbook_name;
            return this._store.query({
                "cursor" : cursor
            });
        },

        access_api_post_greeting: function(guestbook_name, greeting_message){
           this.guestbookName = guestbook_name;
            return this._store.add({
                "guestbook_name": guestbook_name,
                "greeting_message": greeting_message
            });
        },

        access_api_delete_greeting: function(guestbook_name, greeting_id){
            this.guestbookName = guestbook_name;
            return this._store.remove(greeting_id);
        },

        access_api_get_greeting_detail: function(guestbook_name, greeting_id){
            this.guestbookName = guestbook_name;
            return this._store.get(greeting_id);
        },

        access_api_put_greeting: function(guestbook_name, greeting_id, greeting_message){
            this.guestbookName = guestbook_name;
            this.access_api_get_greeting_detail(guestbook_name, greeting_id);
            return this._store.put({
                "guestbook_name": guestbook_name,
                "greeting_message": greeting_message
            });
        }
    });
});
