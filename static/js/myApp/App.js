define([
    "dojo/_base/config",
    "dojo/_base/window",
    "dojo/_base/array",
    "dojo/parser",
    "dojo/ready",
    "dojo/dom",
    "myApp/view/Guestbook",
    "dojo/domReady!"
], function(config, win, array, parser, ready, dom, Guestbook) {

    ready(function() {
        if (!config.parseOnLoad) {
            parser.parse();
        }

        var guestbook = new Guestbook({"guestbook_name": "default_guestbook"});
        var result = dom.byId("result");
        guestbook.placeAt(result);
    });

});
