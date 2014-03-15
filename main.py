""" main.py is the top level script.

"""



# sys.path includes 'server/lib' due to appengine_config.py
import pprint, logging

from flask import Flask, g, session
from flask import redirect, request
from flask import render_template, url_for
from werkzeug.local import LocalProxy

from model import db, raw_db, SearchConstants
from forms import SearchForm, AdvancedSearchForm, AddCollectionForm
from controller import Manager
from settings import config
import json


def build_application():
    app = Flask(config().app_name)

    app.config.update(config().config_dict)
    app.debug = True
    db.init_app(app)
    raw_db.init_app(app, "RAWMONGODB")

    return app


app = build_application()


def get_manager(test_only=False):
    m_manager = getattr(g, '_manager', None)

    if m_manager is None:
        m_manager = Manager(config(test_only=test_only), db, raw_db)

    return m_manager


manager = LocalProxy(get_manager)


def get_search_parameters():
    if "search" in request.args:

        search_values = dict()
        search_values["search"] = request.args.get("search")
        search_values["id"] = None

        if request.args.get("page"):
            search_values["page"] = request.args.get("page")



        if request.args.get("id"):
            search_values["id"] = request.args.get("id")

        if request.args.get("collection"):
            search_values["collection"] = request.args.get("collection")


        if request.args.get("object"):
            search_values["object"] = request.args.get("object")


        #Get Commands
        search_values["commands"] = []

        if request.args.get("command-1"):
            search_values["commands"].append({request.args.get("command-1-type"):json.loads(request.args.get("command-1"))})

            search_values["type"]= SearchConstants.AGGREGATE



        if request.args.get("command-2"):
            search_values["commands"].append({request.args.get("command-2-type"):json.loads(request.args.get("command-2"))})

            search_values["type"]= SearchConstants.AGGREGATE

        if request.args.get("type"):
            search_values["type"] = request.args.get("type")



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


@app.route('/admin', methods=['GET', 'POST'])
def update_settings_page():
    """ Return template at application root URL."""
    template_values = {}

    return render_template('admin.html', **template_values)

    #return redirect(url_for('login_page'))

@app.route('/admin/collections', methods=['GET', 'POST'])
def update_collection_settings_page():
    """ Return template at application root URL."""

    collection_names = {}

    for name in manager.get_raw_collections():
        collection_names[name]= name
    template_values = {}
    if request.method == 'POST':

        form = AddCollectionForm(request.form, csrf_context=session)
        form.collection.choices = collection_names.iteritems()

        if form.validate():

            manager.add_collection(form.label.data, form.collection.data)
            return redirect(url_for('update_settings_page'))
        else:

            template_values["form"] = form
            return render_template('admin_collections.html', **template_values)

    else:

        form = AddCollectionForm(csrf_context=session)
        form.collection.choices = collection_names.iteritems()
        template_values["form"] = form
        return render_template('admin_collections.html', **template_values)

    #return redirect(url_for('login_page'))


@app.route('/')
def landing_page(name=None):
    return render_template('landing.html')

@app.route('/search', methods=['GET'])
def search_page():
    """ Return hello template at application root URL."""
    search = get_search_parameters()
    page_data = {}

    page_data["form"] = SearchForm(csrf_context=session)
    page_data["collections"] = manager.get_available_collections()
    page_data["result"] = None

    if search:
        result = manager.search(search)
        page_data["result"] = result.results
        page_data["headers"] = result.headers

        page_data["raw_results"] = pprint.pformat(result.raw_results)
        page_data["search"] = search["search"]

    return render_template('search.html', **page_data)


@app.route('/advanced', methods=['GET','POST'])
def advanced_page():
    """ Return hello template at application root URL."""
    search = get_search_parameters()
    page_data = {}

    page_data["form"] = AdvancedSearchForm(csrf_context=session)
    page_data["collections"] = manager.get_available_collections()
    page_data["result"] = None
    page_data["command_options"] = manager.get_available_commands()

    if search:
        logging.debug("Started Search")
        result = manager.search(search)
        page_data["result"] = result.results
        page_data["headers"] = result.headers

        page_data["raw_results"] = pprint.pformat(result.raw_results)
        page_data["search"] = search["search"]

    return render_template('advanced.html', **page_data)




if __name__ == "__main__":
    app.run()