from fasthtml.common import *

app, rt = fast_app()


@rt("/")
def get():
    return Div(P("Hello n03an.me"), hx_get="/change")


serve()
