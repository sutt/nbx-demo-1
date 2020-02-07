import os

def get_nb_name(strategy='last'):
    '''
         return a string representing the notebooks filename

         strategy (string) - if multiple nb's, which one to take:
            'last'  - take last notebook in alphanum order
            'first' - take first notebokk in alphanum order
    '''
    
    files = os.listdir('.')
    
    nb_files = [f for f in files if '.ipynb' in f]

    os.path.abspath('.')
    
    if len(nb_files) < 1:
        msg = f'''unable to find any notebook file in current working dir: {os.path.abspath('.')}\n'''
        msg += '''specify a notebook name when calling get_answer(nb_name=) or give_answer(nb_name=)'''
        raise Exception(msg)
                            
    nb_files.sort(reverse=False)

    if strategy == 'last':
        return nb_files[-1]
    elif strategy == 'first':
        return nb_files[0]
    else:
        raise Exception('no `strategy` specified in get_nb_name')
    

