from zope import interface
from zope import component

import manager
import interfaces

def handler(directory, layer):
    lookup_all = component.getGlobalSiteManager().adapters.lookupAll

    # check if a template manager already exists
    factories = set(factory for name, factory in lookup_all(
        (layer,), interfaces.ITemplateManager))

    # if factory is available on the interface bases of the layer we
    # discard it and register a new manager specialized to the layer
    if layer is interface.Interface:
        base_factories = set()
    else:
        base_factories = set()
        for base in layer.__bases__:
            for name, factory in lookup_all((base,), interfaces.ITemplateManager):
                base_factories.add(factory)

    try:
        factory = factories.difference(base_factories).pop()
    except KeyError:
        name = directory
        factory = manager.TemplateManagerFactory(name)
        component.provideAdapter(
            factory, (layer,), interfaces.ITemplateManager, name=name)

    factory(layer).registerDirectory(directory)

    return factory(layer)

def templateOverridesDirective(_context, directory, layer=interface.Interface):
    _context.action(
        discriminator = ('override', directory, layer),
        callable = handler,
        args = (directory, layer),
        )
