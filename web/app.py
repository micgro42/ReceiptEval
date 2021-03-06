#!/usr/bin/env python

import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from entry import form_view
from statistics import statistics_view

here = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    settings = dict(reload_templates=True)
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('entry_route', '/')
    config.add_view(form_view, route_name='entry_route', renderer=os.path.join(here, 'form.pt'))
    config.add_route('statistics_route', 'statistics/')
    config.add_view(statistics_view, route_name='statistics_route',renderer=os.path.join(here, 'form.pt'))
    config.add_static_view('static', 'deform:static')
    config.add_static_view('js', path='js')
    config.add_static_view('css', path='css')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

