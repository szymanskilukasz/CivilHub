//
// config.js
// =========
//
// Konfiguracja dla plików wejściowych dla skryptów, znajdujących się w katalogu
// js/src. Osobna konfiguracja dla buildów znajduje się w pliku config.json.
// Niestety, 'path' i 'shim' muszą się powtarzać, więc jak dodajemy coś do jednego
// pliku, trzeba wprowadzić zmianę w drugim.

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    "paths": {
        "jquery": "includes/jquery/jquery",
        "jqueryui": "includes/jquery-ui/jquery-ui",
        "jpaginate": "includes/jquery/jquery.paginate",
        "bootstrap": "includes/bootstrap/bootstrap",
        "bootbox": "includes/bootstrap/bootbox",
        "underscore": "includes/underscore/underscore",
        "backbone": "includes/backbone/backbone",
        "paginator": "includes/backbone/backbone.paginator",
        "moment": "includes/momentjs/moment",
        "tagsinput": "includes/jquery/jquery.tagsinput",
        "bootstrap-switch" : "includes/bootstrap/bootstrap-switch",
        "redactor": "includes/redactor/redactor",
        "dropzone": "includes/dropzone/dropzone",
        "leaflet": "includes/leaflet/leaflet",
        "fullpagejs": "includes/fullpagejs/jquery.fullPage",
        "color": "includes/jquery/jquery.color",
        "Jcrop": "includes/jquery/jquery.Jcrop",
        "file-input": "includes/bootstrap/bootstrap.file-input",
        "vector": "includes/vectormap/jquery-jvectormap-1.2.2.min",
        "worldmap": "includes/vectormap/jquery-jvectormap-world-mill-en",
        "plot": "includes/jqplot/jquery.jqplot",
        "dateAxisRenderer": "includes/jqplot/plugins/jqplot.dateAxisRenderer",
        "canvasTextRenderer": "includes/jqplot/plugins/jqplot.canvasTextRenderer",
        "canvasAxisTickRenderer": "includes/jqplot/plugins/jqplot.canvasAxisTickRenderer",
        "categoryAxisRenderer": "includes/jqplot/plugins/jqplot.categoryAxisRenderer",
        "barRenderer": "includes/jqplot/plugins/jqplot.barRenderer",
        "tubular": "includes/tubular/jquery.tubular.1.0",
        "tour": "includes/tour/bootstrap-tour",
        "hammer": "includes/mapplic/hammer",
        "jeasing": "includes/mapplic/jquery.easing",
        "mapplic": "includes/mapplic/mapplic",
        "jmousewheel": "includes/mapplic/jquery.mousewheel"
    },

    "shim": {

        "jqueryui": {
            "deps": ["jquery"]
        },

        "tagsinput": {
            "deps": ["jqueryui"]
        },
        
        "jpaginate": {
            "deps": ["jquery"]
        },
        
        "underscore": {
            "deps": ["jquery"],
            "exports": "_"
        },
        
        "backbone": {
            "deps": ["underscore"],
            "exports": "Backbone"
        },
        
        "bootstrap": {
            "deps": ["jquery"]
        },
        
        "bootbox": {
            "deps": ["bootstrap"],
            "exports": "bootbox"
        },

        "bootstrap-switch": {
            "deps": ["bootstrap"]
        },

        "fullpagejs": {
            "deps": ["jquery"]
        },
        
        "color": {
            "deps": ["jquery"]
        },
        
        "Jcrop": {
            "deps": ["color"]
        },
        
        "file-input": {
            "deps": ["bootstrap"]
        },
        
        "vector": {
            "deps": ["jquery"]
        },
        
        "worldmap": {
            "deps": ["vector"]
        },

        "hammer": {
            "deps": ["jquery"]
        },

        "jeasing": {
            "deps": ["jquery"]
        },

        "jmousewheel": {
            "deps": ["jquery"]
        },

        "mapplic": {
            "deps": ["jquery"]
        },
        
        "plot": {
            "deps": ["jquery"]
        },
        
        "dateAxisRenderer": { "deps": ["plot"] },
        "canvasTextRenderer": { "deps": ["plot"] },
        "canvasAxisTickRenderer": { "deps": ["plot"] },
        "categoryAxisRenderer": { "deps": ["plot"] },
        "barRenderer": { "deps": ["plot"] }
    }
});