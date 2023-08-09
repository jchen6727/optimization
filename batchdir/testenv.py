from pubtk.runtk.utils import create_script
from pubtk.runtk.template import sh_template

import json

config = {'netParams.connParams.PYR->BC_AMPA.weight': 1,
          'cfg.flag': True, 'cfg.value': 2, 
          'cfg.dict': json.dumps(dict(one=1, two=2))}

netm_env = {"NETM{}".format(i): 
            "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}

create_script(env = netm_env, 
              filename = 'test.sh',
              template = sh_template,
              header = '', 
              command = '',
              footer = '')

