/**
 * @author Artur Konstanczak
 * @copyright Copyright � 2010, Fry-It, All rights reserved.
 */


(function() {
    // Load plugin specific language pack
    //tinymce.PluginManager.requireLangPack('flags');

    tinymce.create('tinymce.plugins.portlet', {

    /**
         * Initializes the plugin, this will be executed after the plugin has been created.
         * This call is done before the editor instance has finished it's initialization so use the onInit event
         * of the editor instance to intercept that event.
         *
         * @param {tinymce.Editor} ed Editor instance that the plugin is initialized in.
         * @param {string} url Absolute URL to where the plugin is located.
         */
        init : function(ed, url) 
        {

            ed.onInit.add(function(ed) 
            {
              var dom = ed.dom;
              var container = ed.getContainer(); 
              var formfield = dom.getParent(container,'div#formfield-form-text');
              if (formfield != null)
                dom.addClass(ed.getBody(),'text-portlet');
            })

        },

    /**
         * Returns information about the plugin as a name/value array.
         * The current keys are longname, author, authorurl, infourl and version.
         *
         * @return {Object} Name/value array containing information about the plugin.
         */
        getInfo : function() 
        {
            return {
                longname : 'Portlet plugin',
                author : 'Fry-It',
                authorurl : 'http://fry-it.com',
                infourl : 'http://plone.org/products/tinymce',
                version : "1.0"
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('portlet', tinymce.plugins.portlet);
})();