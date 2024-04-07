from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings


def key_bindings(elkcli):
    """
    Create a set of key bindings.

    Args:
        None

    Returns:
        KeyBindings: The key bindings
    """
    # Create a set of key bindings.
    bindings = KeyBindings()

    @bindings.add("c-t")
    def _(event):
        """
        Accept the selected suggestion.

        Args:
            event: The event object

        Returns:
            Nothing
        """
        b = event.current_buffer
        b.accept_suggestion()

    @bindings.add("f4")
    def _(event):
        """
        Toggle between Emacs and Vi mode.

        Args:
            event: The event object

        Returns:
            Nothing
        """
        if elkcli.key_bindings == EditingMode.VI:
            event.app.editing_mode = EditingMode.EMACS
            elkcli.key_bindings = EditingMode.EMACS
        else:
            event.app.editing_mode = EditingMode.VI
            elkcli.key_bindings = EditingMode.VI

    return bindings
