from django.shortcuts import render_to_response
def style(request, stylesheet):
    """
    Render and return the CSS stylesheets as regular rendered templates.

    While the django documentation recommends serving stylesheets, images 
    and other static content from a separate webserver, I believe this make that 
    this makes little sense for small projects. Indeed, on a server 
    configuration where static content is served from a different location 
    from dynamic content, this makes little project management sense.
    """
    return render_to_response("style/"+stylesheet,\
                mimetype="text/css")

def script(request, script):
    """
    Render and return the javascript as regular rendered templates.
    """
    return render_to_response("script/"+script,\
               mimetype="text/javascript")
