def load_blueprints(app, path, bp_attr='module', url_prefix='URL_PREFIX'):
    dir_list = os.listdir(path)
    mods = {}
    with app.app_context():
        for fname in dir_list:
            if fname in (app.config.get('SKIP_BLUEPRINTS') or []):
                continue
            try:
                if os.path.isdir(os.path.join(path, fname)) and os.path.exists(os.path.join(path, fname, '__init__.py')):
                    f, filename, descr = imp.find_module(fname, [path])
                    mods[fname] = imp.load_module(fname, f, filename, descr)
                    app.register_blueprint(
                        getattr(mods[fname], bp_attr),
                        url_prefix=getattr(mods[fname], url_prefix, '/')
                    )
                elif os.path.isfile(os.path.join(path, fname)):
                    name, ext = os.path.splitext(fname)
                    if ext == '.py' and not name == '__init__':
                        f, filename, descr = imp.find_module(name, [path])
                        mods[fname] = imp.load_module(name, f, filename, descr)
                        app.register_blueprint(
                            getattr(mods[fname], bp_attr),
                            url_prefix=getattr(mods[fname], url_prefix, '/')
                        )
            except Exception as e:
                logging.getLogger(__name__).error('Error loading module %s: %s', fname, e)
