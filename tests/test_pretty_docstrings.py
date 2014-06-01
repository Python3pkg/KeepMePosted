import testing
import kemepo; kemepo.set_docstring_formatter('pretty')
import docstring_helpers; docstring_helpers.reload_module(docstring_helpers)
from docstring_helpers import *

@testing.test
def test_pretty_docstrings():
    test_docstring(DocumentedPublisher, # (fold)
            '''\
Docstring for the DocumentedPublisher class.

Events
------
on_first_event
    Called when the first kind of event happens.

on_second_event
    Called when the second kind of event happens.  Line wrapping should
    work and no weird spaces should be inserted.

This class tests the standard case where the events that have been 
registered by this class are added to the docstring.''')

    test_docstring(DocumentedPublisherWithArguments, # (fold)
            '''\
Docstring for the DocumentedPublisherWithArguments class.

Events
------
on_normal_args : first, second
    This event takes two normal arguments.

on_default_values : first, second=None
    Some of this events arguments have default values.

on_varargs : arg, *varargs
    This event takes keyword arguments.

on_kwargs : arg, **kwargs
    This event takes keyword arguments.

This class tests the case where the events being documented have 
complicated argument signatures that should be clearly documented.''')

    test_docstring(DocumentedPublisherWithInheritedEvents, # (fold)
            '''\
Docstring for the DocumentedPublisherWithInheritedEvents class.

Events
------
on_first_event
    Called when the first kind of event happens.

on_second_event
    Called when the second kind of event happens.  Line wrapping should
    work and no weird spaces should be inserted.

on_third_event
    Called when the third kind of event happens.

This class tests the case where inherited events need to be documented 
along with class-specific ones.''')

    test_docstring(DocumentedPublisherWithNoEvents, # (fold)
            '''\
Docstring for the DocumentedPublisherWithNoEvents class.

Events
------
None defined.

This class tests the case where event documentation is requested, but 
there are no events to document.''')

    test_docstring(UndocumentedPublisher, # (fold)
            '''\
Docstring for the UndocumentedPublisher class.

This class tests the case where a event documentation is not generated, 
even though a few events are defined.''')


