""" main.py is the top level script.

"""



# sys.path includes 'server/lib' due to appengine_config.py
import pprint

from flask import Flask, g, session
from flask import redirect, request
from flask import render_template
from werkzeug.local import LocalProxy

from model import db, raw_db
from forms import SearchForm
from controller import Manager
from settings import config


def build_application():
    app = Flask(config().app_name)

    app.config.update(config().config_dict)
    app.debug = True
    db.init_app(app)
    raw_db.init_app(app, "RAWMONGODB")

    return app


app = build_application()


def get_manager():
    m_manager = getattr(g, '_manager', None)

    if m_manager is None:
        m_manager = Manager(config(test_only=True), db, raw_db)

    return m_manager


manager = LocalProxy(get_manager)


def get_search_parameters():
    if "search" in request.args:

        search_values = dict()
        search_values["search"] = request.args.get("search")

        if request.args.get("page"):
            search_values["page"] = request.args.get("page")

        if request.args.get("collection"):
            search_values["collection"] = request.args.get("collection")

        return search_values
    else:
        return None


@app.route('/logout')
def logout_page(name=None):
    """ Return hello template at application root URL."""

    return redirect("./")


@app.route('/login')
def login_page(name=None):
    return render_template('login.html', name=name)


@app.route('/settings', methods=['GET', 'POST'])
def update_settings_page():
    """ Return template at application root URL."""
    template_values = {}

    return render_template('settings.html', **template_values)

    #return redirect(url_for('login_page'))


@app.route('/fresh', methods=['GET'])
def landing_page():
    """ Return hello template at application root URL."""
    search = get_search_parameters()
    page_data = {}

    page_data["form"] = SearchForm(csrf_context=session)
    page_data["collections"] = manager.get_available_collections()

    page_data["results"] = None
    if search:
        results, headers, raw_results = manager.search(search)
        page_data["results"] = results
        page_data["headers"] = headers

        page_data["raw_results"] = pprint.pformat(raw_results)
        page_data["search"] = search["search"]

    return render_template('search.html', **page_data)


@app.route('/fresh/aggregatr/', methods=['GET'])
def aggregation_page():
    """ Return hello template at application root URL."""
    search = get_search_parameters()
    page_data = {}

    page_data["results"] = None
    if search:
        results, headers = manager.search(search)
        page_data["results"] = results
        page_data["headers"] = headers

    return render_template('search.html', **page_data)


@app.route('/fresh/mapreduce/', methods=['GET'])
def map_reduce_page():
    """ Return hello template at application root URL."""
    search = get_search_parameters()
    page_data = {}

    page_data["results"] = None
    if search:
        results, headers = manager.search(search)
        page_data["results"] = results
        page_data["headers"] = headers

    return render_template('search.html', **page_data)


@app.route('/refined', methods=['GET'])
def refined_landing_page():
    """ Return hello template at application root URL."""
    search = get_search_parameters()
    page_data = {}

    page_data["form"] = SearchForm(csrf_context=session)
    page_data["collections"] = manager.get_available_objects()

    page_data["results"] = None
    if search:
        results, headers, raw_results = manager.refined_search(search)
        page_data["results"] = results
        page_data["headers"] = headers

        page_data["raw_results"] = pprint.pformat(raw_results)
        page_data["search"] = search["search"]

    return render_template('search.html', **page_data)


if __name__ == "__main__":
    app.run()