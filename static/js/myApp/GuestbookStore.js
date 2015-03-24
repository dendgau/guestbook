define([
    'dojo/Deferred',
    'dojo/_base/xhr',
    'dojo/request/xhr',
    'dojo/cookie',
    'dojo/domReady!'
], function(_Deferred, xhr, xhrRequest, cookie){
    return {
        access_api_get_greeting_detail: function(guestbook_name, greeting){
            var deferred = new _Deferred();

            dojo.xhrGet({
                url: base+"/guestbook_app/guestbook/"+guestbook_name+"/greeting/"+greeting,
                handleAs: "json",
                load: function(data){
                    deferred.resolve(data)
                },
                error: function(error){
                    return deferred.reject(error);
                }
            });

            return deferred.promise;
        },

        access_api_get_list_greeting: function(guestbook_name, url_safe){
            var get_param = ""
            if (url_safe){
                get_param = "?url_safe="+url_safe;
            }
            var url_api = base+"/guestbook_app/guestbook/"+guestbook_name+"/greeting"+get_param;
            var deferred = new _Deferred();

            dojo.xhrGet({
                url: url_api,
                handleAs: "json",
                load: function(data){
                    deferred.resolve(data)
                },
                error: function(error){
                    return deferred.reject(error);
                }
            });

            return deferred.promise;
        },

        access_api_put_greeting: function(){
            alert("Put greeting");
        },

        access_api_post_greeting: function(){
            alert("Post greeting");
        },

        access_api_delete_greeting: function(guestbook_name, greeting){
            var deferred = new _Deferred();

            dojo.xhrDelete({
                url: base+"/guestbook_app/guestbook/"+guestbook_name+"/greeting/"+greeting,
                handleAs: "json",
                headers: {"X-CSRFToken": cookie("csrftoken")},
                load: function(data){
                    deferred.resolve("Delete Success")
                },
                error: function(error){
                    return deferred.reject(error);
                }
            });

            return deferred.promise;
        }
    };
});
