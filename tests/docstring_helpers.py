from kemepo import Dispatcher, event
from six.moves import reload_module

class DocumentedPublisher (Dispatcher):
    """ 
    Docstring for the DocumentedPublisher class.
    
    {events}

    This class tests the standard case where the events that have been 
    registered by this class are added to the docstring.
    """

    @event
    def on_first_event(self):
        """ Called when the first kind of event happens. """
        pass

    @event
    def on_second_event(self):
        """ Called when the second kind of event happens.  Line wrapping 
        should work and no weird spaces should be inserted. """
        pass


class DocumentedPublisherWithArguments (Dispatcher):
    """ 
    Docstring for the DocumentedPublisherWithArguments class.

    {events}

    This class tests the case where the events being documented have 
    complicated argument signatures that should be clearly documented.
    """

    @event
    def on_normal_args(self, first, second):
        """ This event takes two normal arguments. """
        pass

    @event
    def on_default_values(self, first, second=None):
        """ Some of this events arguments have default values. """
        pass

    @event
    def on_varargs(self, arg, *varargs):
        """ This event takes keyword arguments. """
        pass

    @event
    def on_kwargs(self, arg, **kwargs):
        """ This event takes keyword arguments. """
        pass


class DocumentedPublisherWithInheritedEvents (DocumentedPublisher):
    """ 
    Docstring for the DocumentedPublisherWithInheritedEvents class.

    {events}

    This class tests the case where inherited events need to be documented 
    along with class-specific ones.
    """

    @event
    def on_third_event(self):
        """ Called when the third kind of event happens. """
        pass


class DocumentedPublisherWithNoEvents (Dispatcher):
    """ 
    Docstring for the DocumentedPublisherWithNoEvents class.

    {events}

    This class tests the case where event documentation is requested, but 
    there are no events to document.
    """
    pass

class UndocumentedPublisher (Dispatcher):
    """ 
    Docstring for the UndocumentedPublisher class.

    This class tests the case where a event documentation is not generated, 
    even though a few events are defined.
    """

    @event
    def on_first_event(self):
        """ Called when the first kind of event happens. """
        pass

    @event
    def on_second_event(self):
        """ Called when the second kind of event happens.  This different
        from the first kind of event, because it happens second. """
        pass



class ExplicitSphinxDocstring (Dispatcher):
    """ 
    Docstring for the DocumentedPublisherWithArguments class.

    :events:
        **on_normal_args** : first, second
            This event takes two normal arguments.

        **on_default_values** : first, second=None
            Some of this events arguments have default values.

        **on_varargs** : arg, *varargs
            This event takes keyword arguments.

        **on_kwargs** : arg, **kwargs
            This event takes keyword arguments.

    This class tests the case where the events being documented have 
    complicated argument signatures that should be clearly documented.
    """


def test_docstring(cls, expected_docstring):
    import difflib

    expected_docstring = expected_docstring.strip()
    expected_lines = expected_docstring.splitlines(True)

    actual_docstring = cls.__doc__
    actual_lines = actual_docstring.splitlines(True)

    differ = difflib.Differ()
    diff_lines = differ.compare(expected_lines, actual_lines)

    error_message = "Diff between actual and expected docstrings:\n\n"
    for line in diff_lines: error_message += line

    assert expected_docstring == actual_docstring, error_message


