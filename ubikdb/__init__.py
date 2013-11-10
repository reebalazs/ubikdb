#

def monkey_patch():
    # Monkey-patch gevent
    from gevent import monkey
    print monkey.patch_all()
monkey_patch()

