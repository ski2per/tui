import urwid
from tui import conf


class ComponentChoice(urwid.WidgetWrap):
    signals = ['install_event']

    def __init__(self):
        self.options = []
        self.warning = urwid.Text('')
        self._components = []

        # To use 'user_data', set 'on_state_change'
        checkboxes = []
        for key, title in conf.COMPONENTS.items():
            checkboxes.append(
                urwid.CheckBox(title, on_state_change=self._handle_checkbox_change, user_data=key)
            )
        choice = urwid.Pile(checkboxes)

        wrapped_btn = urwid.AttrWrap(urwid.Button('Install', on_press=self._handle_button_click), 'button')
        install_btn = urwid.Padding(wrapped_btn, width=('relative', 10), align='left', min_width=12)

        content = [
            urwid.Divider(top=conf.DEFAULT_TOP_PADDING),
            urwid.Text(('error', 'Choose Component to Install:')),
            urwid.Divider(),
            choice,
            urwid.Divider(),
            urwid.AttrWrap(self.warning, 'warning'),
            urwid.Divider(),
            install_btn
        ]

        widget = urwid.Padding(urwid.ListBox(urwid.SimpleListWalker(content)), width=('relative', 50), align="center")
        # widget = urwid.AttrWrap(widget, 'body')
        urwid.WidgetWrap.__init__(self, widget)

    def _handle_checkbox_change(self, *args):
        _, state, label = args
        if state:
            if label not in self._components:
                self._components.append(label)
        else:
            try:
                self._components.remove(label)
            except ValueError:
                pass

    def _handle_button_click(self, *args):
        if self._components:
            self._emit('install_event', args)
        else:
            self.warning.set_text('Choose component to install')

    @property
    def components(self):
        return self._components
