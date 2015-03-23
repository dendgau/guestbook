define([
    'dojo/Deferred',
    'dojo/_base/xhr',
    'dojo/domReady!'
], function(_Deferred, xhr){
    return {
        access_api_get_greeting_detail: function(){
            var deferred = new _Deferred();

            xhr.get({
                url: base+"/guestbook_app/guestbook/default_guestbook/greeting/4785074604081152",
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

        access_api_get_list_greeting: function(){
            alert("Get list greeting");
        },

        access_api_put_greeting: function(){
            alert("Put greeting");
        },

        access_api_post_greeting: function(){
            alert("Post greeting");
        },

        access_api_delete_greeting: function(){
            alert("Delete greeting");
        }
    };
});
