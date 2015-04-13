from __future__ import print_function

import sys
import os
import json
import io

from IPython.utils.py3compat import cast_unicode_py2
import jupyter_notebook.nbextensions as nbe
from jupyter_core.paths import jupyter_config_dir
from traitlets.config import Config, JSONFileConfigLoader, ConfigFileNotFound


def install(symlink=True, mixed=False, user=False, prefix=None,
            verbose=False, path=None):
    dname = os.path.dirname(__file__)
    pdir = jupyter_config_dir()

    # miht want to check if already installed and overwrite if exist
    if symlink and verbose:
        print('Will try symlink nbextension')
    if mixed and verbose:
        print('Will install mixed content manager')
    if prefix and verbose:
        print("I'll install in prefix:", prefix)
    nbe.install_nbextension(os.path.join(dname,'gdrive'),
                                symlink=symlink,
                                   user=user,
                                 prefix=prefix,
                                 nbextensions_dir=path)

    jc = JSONFileConfigLoader('jupyter_notebook_config.json',pdir)


    try:
        config = jc.load_config();
    except (ConfigFileNotFound,ValueError) as e:
        config = Config()
    if 'NotebookApp' in config:
        if ('tornado_settings' in config['NotebookApp']) or ('contents_manager_class' in config['NotebookApp']):
            # TODO, manually merge tornado settin if exist
            # but cannot do anythin automatically if contents_manager_calss is set
            raise ValueError('You already got some configuration that will conflict with google drive. Bailin out')
    if mixed :
        drive_config  = JSONFileConfigLoader('mixed_contents.json', dname).load_config()
    else :
        drive_config  = JSONFileConfigLoader('ipython_notebook_config.json', dname).load_config()
    config.merge(drive_config)
    print('Activating Google Drive integration for profile "%s"' % profile)
    config['nbformat'] = 1

    print('Activating Google Drive integration')
    with io.open(os.path.join(pdir,'jupyter_notebook_config.json'),'w', encoding='utf-8') as f:
        f.write(cast_unicode_py2(json.dumps(config, indent=2)))

def deactivate(profile):
    """should be a matter of just unsetting the above keys
    """

    raise NotImplemented('deactivating a profile is not yet implemented.')


def main(argv=None):
    import argparse
    prog = '{} -m jupyterdrive'.format(os.path.basename(sys.executable))
    parser = argparse.ArgumentParser(prog=prog,
                    description='Install Google Drive integration for Jupyter.')
    parser.add_argument("-m", "--mixed", help="Installed the mixed content manager",
                    action="store_true")
    parser.add_argument("-S", "--no-symlink", help="do not symlink at install time",
                    action="store_false", dest='symlink', default=True)
    parser.add_argument("-u", "--user", help="force install in user land",
                    action="store_true")
    parser.add_argument("-p", "--prefix", help="Prefix where to install extension",
                    action='store', default=None)
    parser.add_argument("-P", "--path", help="explicit path on where to install the extension",
                    action='store', default=None)
    parser.add_argument("-v", "--verbose", help="increase verbosity",
                    action='store_true')
    args = parser.parse_args(argv)

    install(   path=args.path,
              mixed=args.mixed,
            prefix=args.prefix,
            symlink=args.symlink,
            verbose=args.verbose
            )
