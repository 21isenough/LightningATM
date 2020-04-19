import kivy

from kivy.app import App

import graphicpage


class GraficApp(App):
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#
#        self.page1 = graphicpage.Page()

    def build(self):
        self.page1 = graphicpage.Page()
        return self.page1