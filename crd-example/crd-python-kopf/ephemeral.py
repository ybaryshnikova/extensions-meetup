import kopf
import handlers


@kopf.on.create('ephemeralvolumeclaims', retries=1)
def create_fn(spec, name, namespace, logger, **kwargs):
    return handlers.create_fn(spec, name, namespace, logger)


@kopf.on.update('ephemeralvolumeclaims', retries=1)
def update_fn(spec, status, namespace, logger, **kwargs):
    print(f"STATUS {status}")
    handlers.update_fn(spec, status, namespace, logger)


# @kopf.on.field('ephemeralvolumeclaims', field='metadata.labels')
# def relabel(old, new, status, namespace, **kwargs):

# @kopf.on.field('ephemeralvolumeclaims', field='spec.size', retries=1)
