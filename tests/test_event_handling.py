#!/usr/bin/env python3



import testing, contextlib
from kemepo import event, Dispatcher

def make_note(message):
    make_note.messages.append(message)
    print(message)

@contextlib.contextmanager
def record_notes():
    make_note.messages = []
    yield make_note.messages


class ParentPublisher (Dispatcher):

    @event
    def on_parent_event(self, message):
        make_note('ParentPublisher.on_parent_event({})'.format(message))

    @event
    def on_argless_event(self):
        make_note('ParentPublisher.on_argless_event()')

    @event
    def on_varargs_event(self, *varargs):
        varargs_str = ', '.join(str(x) for x in varargs)
        make_note('ParentPublisher.on_varargs_event({})'.format(varargs_str))

    @event
    def on_kwargs_event(self, **kwargs):
        kw_items = sorted(kwargs.items())
        kwargs_str = ', '.join('{}={}'.format(*x) for x in kw_items)
        make_note('ParentPublisher.on_kwargs_event({})'.format(kwargs_str))


class ChildPublisher (ParentPublisher):

    @event
    def on_child_event(self, message):
        make_note('ChildPublisher.on_child_event({})'.format(message))


class Observer:

    def on_parent_event(self, message):
        make_note('Observer.on_parent_event({})'.format(message))

    def on_child_event(self, message):
        make_note('Observer.on_child_event({})'.format(message))

    def irrelevant_method(self):
        pass



@testing.test
def test_observer_function():
    def observer(message):
        make_note("observer({})".format(message))

    with record_notes() as notes:
        publisher = ParentPublisher()
        publisher.connect(on_parent_event=observer)
        publisher.handle('on_parent_event', 'hello')
        publisher.notify('on_parent_event', 'hello')
        publisher.disconnect(observer)
        publisher.handle('on_parent_event', 'goodbye')
        publisher.notify('on_parent_event', 'goodbye')

    assert len(notes) == 4
    assert notes[0] == 'ParentPublisher.on_parent_event(hello)'
    assert notes[1] == 'observer(hello)'
    assert notes[2] == 'observer(hello)'
    assert notes[3] == 'ParentPublisher.on_parent_event(goodbye)'

@testing.test
def test_observer_lambda_function():
    observer = lambda message: make_note('lambda({})'.format(message))

    with record_notes() as notes:
        publisher = ParentPublisher()
        publisher.connect(on_parent_event=observer)
        publisher.handle('on_parent_event', 'hello')
        publisher.notify('on_parent_event', 'hello')
        publisher.disconnect(observer)
        publisher.handle('on_parent_event', 'goodbye')
        publisher.notify('on_parent_event', 'goodbye')

    assert len(notes) == 4
    assert notes[0] == 'ParentPublisher.on_parent_event(hello)'
    assert notes[1] == 'lambda(hello)'
    assert notes[2] == 'lambda(hello)'
    assert notes[3] == 'ParentPublisher.on_parent_event(goodbye)'

@testing.test
def test_observer_object():
    with record_notes() as notes:
        publisher = ParentPublisher()
        observer = Observer()

        publisher.connect(observer)
        publisher.handle('on_parent_event', 'hello')
        publisher.notify('on_parent_event', 'hello')
        publisher.disconnect(observer)
        publisher.handle('on_parent_event', 'goodbye')
        publisher.notify('on_parent_event', 'goodbye')

    assert len(notes) == 4
    assert notes[0] == 'ParentPublisher.on_parent_event(hello)'
    assert notes[1] == 'Observer.on_parent_event(hello)'
    assert notes[2] == 'Observer.on_parent_event(hello)'
    assert notes[3] == 'ParentPublisher.on_parent_event(goodbye)'

@testing.test
def test_inherited_events():
    with record_notes() as notes:
        publisher = ChildPublisher()
        observer = Observer()

        publisher.connect(observer)
        publisher.handle('on_parent_event', 'hello')
        publisher.notify('on_parent_event', 'hello')
        publisher.handle('on_child_event', 'bonjour')
        publisher.notify('on_child_event', 'bonjour')

    assert len(notes) == 6
    assert notes[0] == 'ParentPublisher.on_parent_event(hello)'
    assert notes[1] == 'Observer.on_parent_event(hello)'
    assert notes[2] == 'Observer.on_parent_event(hello)'
    assert notes[3] == 'ChildPublisher.on_child_event(bonjour)'
    assert notes[4] == 'Observer.on_child_event(bonjour)'
    assert notes[5] == 'Observer.on_child_event(bonjour)'

@testing.test
def test_illegal_arguments():
    publisher = ChildPublisher()

    publisher.handle('on_argless_event')
    publisher.handle('on_parent_event', 1)
    publisher.handle('on_varargs_event')
    publisher.handle('on_varargs_event', 1)
    publisher.handle('on_varargs_event', 1, 2)
    publisher.handle('on_kwargs_event', a=1, b=2)

    with testing.expect(TypeError):
        publisher.handle('on_parent_event')

    with testing.expect(TypeError):
        publisher.handle('on_argless_event', 1, 2)
    with testing.expect(TypeError):
        publisher.handle('on_parent_event', 1, 2)
    with testing.expect(TypeError):
        publisher.handle('on_kwargs_event', 1, 2)

    with testing.expect(TypeError):
        publisher.handle('on_argless_event', a=1, b=2)
    with testing.expect(TypeError):
        publisher.handle('on_parent_event', a=1, b=2)
    with testing.expect(TypeError):
        publisher.handle('on_varargs_event', a=1, b=2)

@testing.test
def test_illegal_observers():
    publisher = ChildPublisher()

    publisher.connect(on_argless_event=lambda: None)
    publisher.connect(on_parent_event=lambda arg: None)
    publisher.connect(on_varargs_event=lambda *varargs: None)
    publisher.connect(on_kwargs_event=lambda **kwargs: None)

    with testing.expect(TypeError):
        publisher.connect(on_parent_event=lambda: None)
    with testing.expect(TypeError):
        publisher.connect(on_varargs_event=lambda: None)
    with testing.expect(TypeError):
        publisher.connect(on_kwargs_event=lambda: None)

    with testing.expect(TypeError):
        publisher.connect(on_argless_event=lambda arg: None)
    with testing.expect(TypeError):
        publisher.connect(on_varargs_event=lambda arg: None)
    with testing.expect(TypeError):
        publisher.connect(on_kwargs_event=lambda arg: None)

    with testing.expect(TypeError):
        publisher.connect(on_parent_event=lambda *varargs: None)
    with testing.expect(TypeError):
        publisher.connect(on_kwargs_event=lambda *varargs: None)

    with testing.expect(TypeError):
        publisher.connect(on_parent_event=lambda **kwargs: None)
    with testing.expect(TypeError):
        publisher.connect(on_varargs_event=lambda **kwargs: None)


