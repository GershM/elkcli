from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.application.current import get_app
from prompt_toolkit.enums import EditingMode


def create_toolbar_tokens_func(elkcli):
    """Return a function that generates the toolbar tokens."""
    def get_toolbar_tokens():
        mode = 'Vi' if elkcli.key_bindings != EditingMode.VI else 'Emacs'
        result = []

        if elkcli.key_bindings == EditingMode.VI:
            result.append(('class:bottom-toolbar.on', ' Vi-mode ({}) | '.format(_get_vi_mode())))

        result.append(('class:bottom-toolbar', ' [F4] %s ' % mode))
        if elkcli.toolbar_error_message:
            result.append(
                ('class:bottom-toolbar', '  ' + elkcli.toolbar_error_message))
            elkcli.toolbar_error_message = None

        return result

    return get_toolbar_tokens


def _get_vi_mode():
    """Get the current vi mode for display."""
    return {
        InputMode.INSERT: 'Insert',
        InputMode.NAVIGATION: 'Normal',
        InputMode.REPLACE: 'Replace',
        InputMode.REPLACE_SINGLE: 'Replace-Single',
        InputMode.INSERT_MULTIPLE: 'Multiple',
    }[get_app().vi_state.input_mode]
