"""
Basic UI for browsing and analyzing files
"""

from yapsy.IPlugin import IPlugin
import os
import logging

class FaAnalyze(IPlugin):

    def __init__(self):
        IPlugin.__init__(self)

    def activate(self):
        IPlugin.activate(self)
        return

    def deactivate(self):
        IPlugin.deactivate(self)
        return

    def display_name(self):
        """Returns the name displayed in the webview"""
        return "File Analyze"

    def check(self, curr_file, path_on_disk, mimetype, size):
        """Checks if the file is compatable with this plugin"""
        return True

    def mimetype(self, mimetype):
        """Returns the mimetype of this plugins get command"""
        return "text/plain"

    def popularity(self):
        """Returns the popularity which is used to order the apps from 1 (low) to 10 (high), default is 5"""
        return 0

    def parent(self):
        """Returns if the plugin accepts other plugins (True) or only files (False)"""
        return False

    def cache(self):
        """Returns if caching is required"""
        return True

    def get(self, curr_file, helper, path_on_disk, mimetype, size, request, children):
        """Provides a web view with all applicable plugins, defaults to most popular"""
        
        #Add Directoy link
        plugins = []
        plugins.append('<a href="/plugins/fa_loader/fa_overview/' + curr_file['pid'] + '" target="frame">Overview</a><br>')

        if not mimetype:
            mimetype = helper.guess_mimetype(curr_file['ext'])
        if not size and 'file_size' not in curr_file:
            size = 0
        elif not size:
            size = curr_file['file_size'][0]

        #Order Plugins by populatiry from highest to lowest
        for pop in reversed(range(1, 11)):
            for plugin in helper.plugin_manager.getAllPlugins():
                if plugin.plugin_object.popularity() == pop:
                    #Check if plugin applies to curr file
                    if plugin.plugin_object.display_name() != 'Overview' and plugin.plugin_object.check(curr_file, path_on_disk, mimetype, size):
                        logging.debug("Check matched, adding plugin " + plugin.plugin_object.display_name())
                        plugins.append('<a href="/plugins/fa_loader/' + plugin.name + '/' + curr_file['pid'] + '" target="frame">' + plugin.plugin_object.display_name() + '</a><br>')
                    else:
                        logging.debug("Check did not match, NOT adding plugin " + plugin.plugin_object.display_name())

        #Modifies HTML page
        html = ""
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        template = open(curr_dir + '/analyze_template.html', 'r')
        html = str(template.read())
        template.close()
        html = html.replace('<!-- Home -->', "/plugins/fa_loader/fa_overview/" + curr_file['pid'])
        
        if curr_file['meta_type'] == 'Directory':
            html = html.replace('<!-- File -->', curr_file['name'])
            html = html.replace('<!-- Mimetype -->', 'Directory')
            if 'file_size' in curr_file:
                html = html.replace('<!-- Size -->', str(curr_file['file_size'][0]) + " Bytes")
            else:
                html = html.replace('<!-- Size -->', "0 Bytes")
            html = html.replace('<!-- Links -->', "\n".join(plugins))
        else:
            html = html.replace('<!-- File -->', curr_file['name'])
            html = html.replace('<!-- Mimetype -->', mimetype)
            html = html.replace('<!-- Size -->', str(size) + " Bytes")
            html = html.replace('<!-- Links -->', "\n".join(plugins))
        
        return html


