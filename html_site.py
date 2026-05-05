# -*- coding: utf-8 -*-
"""
Kullanici Sitesi CSS ve HTML Template.
Icerik html_site_css.dat ve html_site_template.dat dosyalarindan okunur.
Bu yaklasim Python 3.13 ile JavaScript template literal uyumsuzlugunu onler.
"""

import os as _os

_dir = _os.path.dirname(_os.path.abspath(__file__))

with open(_os.path.join(_dir, 'html_site_css.dat'), 'r', encoding='utf-8') as _f:
    SITE_CSS = _f.read()

with open(_os.path.join(_dir, 'html_site_template.dat'), 'r', encoding='utf-8') as _f:
    SITE_HTML_TEMPLATE = _f.read()
