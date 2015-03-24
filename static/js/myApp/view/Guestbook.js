define([
    "dojo/_base/declare",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
	"dojo/text!./templates/template_guestbook.html",
    "myApp/GuestbookStore",
    "myApp/view/Greeting",
	"dojo/_base/fx",
	"dojo/_base/lang",
    "dijit/form/Button",
    "dijit/form/Form",
    "dijit/form/TextBox",
    "dijit/form/Textarea",
    "dojo/dom",
    "dojo/_base/array",
    "dijit/registry",
    "dojo/query"
], function(declare, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin, template,
            _GuestbookStore, _Greeting, baseFx, lang, _button, _form, _textbox, _textarea, dom, array, registry,query){

        return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {

            templateString: template,
            guestbook_name: "",

            constructor: function(data){
                this.guestbook_name = data.guestbook_name;
            },

            postCreate: function(data){
                var input_switch = registry.byId("textbox_switch");
                input_switch.set("value", this.guestbook_name);
                this._load_greeting_from_guestbook();

                this.inherited(arguments);
            },

            _change_guestbook: function(){
                var input_switch = registry.byId("textbox_switch");
                this.guestbook_name = input_switch.get("value");
                this._load_greeting_from_guestbook();
            },

            _load_greeting_from_guestbook: function(){
                array.forEach(query(".widget_greeting"), function(greeting){
                    var widget = registry.byId(greeting.id);
                    widget.destroy();
                })

                _GuestbookStore.access_api_get_list_greeting(this.guestbook_name, "")
				.then(function(json){
					var result = dom.byId("greetings");
                    var greetings = json.greetings
                    array.forEach(greetings, function(greeting){
                        var data = {
                            "guestbook_name": json.guestbook_name,
							"greeting_id": greeting.greeting_id,
							"updated_by": greeting.greeting_auth,
                            "content": greeting.greeting_content,
							"date": greeting.greeting_date
                        }
						var greeting = new _Greeting(data);
						greeting.placeAt(result);
                        greeting.startup();
					});
				}, function(error){
					alert(error);
                });
            },

            _add_new_greeting: function(){
                var new_content = registry.byId("new_greeting_content");
                _GuestbookStore.access_api_post_greeting(this.guestbook_name,
                    new_content.get("value")).then(function(data){
                        alert(data);
                        this._load_greeting_from_guestbook();
                    }, function(error){
                        alert(error);
                    })
            }
        });
});