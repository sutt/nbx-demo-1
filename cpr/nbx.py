import os, sys, time

from .merge import get_answer
from .merge import give_answer

from .cpr import reload_nb
from .cpr import set_nbname_global

from .gitcomm import pull_answer
from .gitcomm import push_answer

from .utils import get_nb_name


# these don't work: it adds the global to the __main__ scope which 
# is not shareable across modules

# call this when module is loaded to get NBX_NBNAME_GLOBAL 
# set in __main__ context from js
# set_nbname_global()

# def nbname_from_global(nb_name):
#     ''' pull nbname established in set_nbname_global
#         unless nb_name is specificied by user
#     '''
#     if nb_name is not None:
#         return nb_name
#     try:
#         global NBX_NBNAME_GLOBAL
#         return NBX_NBNAME_GLOBAL
#     except:
#         raise Exception('cannot find NBX_NBNAME_GLOBAL')


def receive_answer( nb_name=None, 
                    remote_name='local',
                    b_log=False, 
                    b_replace=False,
                    b_save=False
                    ):
    '''
         all actions to receive [latest] answer
    '''

    if nb_name is None:
        nb_name = get_nb_name(strategy='last')    

    pull_answer(remote_name=remote_name, 
                b_log=b_log,
                )
    
    get_answer( fn_nb=nb_name, 
                term='receive_answer',
                b_replace=b_replace,
                )
    
    reload_nb(  b_save=b_save, 
                b_scroll=True,
                b_flash=True,
                b_select=True,
                b_log=False,
                debug=False,
                )
    


def send_answer( nb_name=None,
                 remote_name='local',
                 b_log=False,
                 ):
    '''
         all actions to append [cell above] as an answer
    '''

    if nb_name is None:
        nb_name = get_nb_name(strategy='last')
    
    give_answer(fn_nb=nb_name, 
                term='send_answer',
                )
    
    push_answer(remote_name=remote_name, 
                b_log=b_log,
                )
    
    print('send_answer done.')