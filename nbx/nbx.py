import os, sys, time

from .merge import get_answer as _get_answer
from .merge import give_answer as _give_answer

from .frontend import reload_nb as _reload_nb

from .gitcomm import pull_answer as _pull_answer
from .gitcomm import push_answer as _push_answer

from .utils import get_nb_name as _get_nb_name

'''
    Module for v1 nbx functionality.
'''



def receive_answer( nb_name=None, 
                    remote_name='origin',
                    b_log=False, 
                    b_replace=False,
                    b_save=False
                    ):
    '''
         all actions to receive [latest] answer
    '''

    if nb_name is None:
        nb_name = _get_nb_name(strategy='last')    

    _pull_answer(remote_name=remote_name, 
                 b_log=b_log,
                 )
    
    _get_answer( fn_nb=nb_name, 
                 term='receive_answer',
                 b_replace=b_replace,
                 )
    
    _reload_nb( b_save=b_save, 
                b_scroll=True,
                b_flash=True,
                b_select=True,
                b_log=False,
                debug=False,
                )
    


def send_answer( nb_name=None,
                 remote_name='origin',
                 b_log=False,
                 ):
    '''
         all actions to append [cell above] as an answer
    '''

    if nb_name is None:
        nb_name = _get_nb_name(strategy='last')
    
    _give_answer(fn_nb=nb_name, 
                 term='send_answer',
                )
    
    _push_answer(remote_name=remote_name, 
                 b_log=b_log,
                )
    
    print('send_answer done.')