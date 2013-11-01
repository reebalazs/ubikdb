#
# Evolve scripts for the sdi_ubikdb_demo
#

import logging

logger = logging.getLogger('evolution')

def say_hello(root):
    logger.info(
        'Running sdi_ubikdb_demo evolve step 1: say hello'
    )

def includeme(config):
    config.add_evolution_step(say_hello)
    
