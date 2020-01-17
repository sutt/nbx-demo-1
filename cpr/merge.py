import os
import json

'''
TODO

[ ] force remote version for merge
'''
CELLS_DIR = '.cpr'
CELLS_JSON = os.path.join(CELLS_DIR, 'cells.json')


def check_directory(cells_dir=CELLS_DIR):
    b_exists = os.path.exists(cells_dir)
    if b_exists:
        return True
    try:
        os.mkdir(CELLS_DIR)
        return True
    except:
        raise Exception(f'failed to make directory {CELLS_DIR}')


def check_file(cells_json=CELLS_JSON):
    return os.path.exists(cells_json)


def find_answer_index(cell_list,
                      term,
                      multi_index_strat = 'last',
                      ):

    ind_terms = [i for i, cell in enumerate(cell_list)
                if any([term in t for t in cell.get('source', [])]) 
                ]
    
    if multi_index_strat == 'last':
        multi_ind = -1
    else:
        multi_ind = -1
    
    if len(ind_terms) < 1:
        print(cell_list)
        raise Exception('failed to find index of cell, maybe save notebook manually? ')
    
    return ind_terms[multi_ind]


def insert_cell(cell_index,
                new_cell,
                nb_json,
                b_replace=True,
               ):
    '''
        
    '''
    new_json = nb_json.copy()
    
    if b_replace:
        try:
            _pop = new_json['cells'].pop(cell_index)
        except:
            print(f'could not remove cell from index: {cell_index}')
    
    try:
        new_json['cells'].insert(cell_index, new_cell)
    except:
        print(f'could not insert new_cell at index: {cell_index}')
    
    return new_json


def give_answer(fn_nb, term='give_answer('):
    '''
        append cell above onto answers
    '''
    
    ec = check_directory()
    if not(ec): raise Exception()

    # Get Answer from teacher notebook
    nb_json = json.load(open(fn_nb, 'r'))

    nb_index = find_answer_index(nb_json['cells'], term=term)
    
    nb_cell = nb_json['cells'][nb_index - 1]   # take cell above

    # Write answer cell into cells.json intermediate representation
    ec = check_file()
    if ec:
        try:
            answer_json = json.load(open(CELLS_JSON, 'r'))
        except:
            raise Exception(f'file exists but unable to load: {CELLS_JSON}')
    else:
        answer_json = json.loads('''{"cells":[]}''')

    answer_json['cells'].append(nb_cell)

    try:
        json.dump(answer_json, open(CELLS_JSON,'w'))
    except Exception as e:
        raise Exception(f'unable to write to {CELLS_JSON}, err: {e}')

    return 
    

def get_answer(fn_nb, term='get_answer', b_replace=True):
    '''
         take last answer
         
         b_replace (bool) - overwrite cell with get_answer() code
    '''
    ec = check_directory()
    if not(ec): raise Exception(f'no answer directory {CELLS_DIR}')
    ec = check_file()
    if not(ec): raise Exception(f'no answer json {CELLS_JSON}')
    
    # Read-in Answers
    try:
        answer_json = json.load(open(CELLS_JSON, 'r'))
    except:
        raise Exception(f'file exists but unable to load: {CELLS_JSON}')
    
    try:
        answer_cell = answer_json['cells'][-1]
    except:
        raise Exception('couldnt find last answer, either no `cells` key or of 0-length')

    
    # Write answer into notbook
    try:
        nb_json = json.load(open(fn_nb, 'r'))
    except:
        raise Exception(f'unable to read current notebook: {fn_nb}')

    try:
        nb_index = find_answer_index(nb_json['cells'], term=term)
    except:
        raise Exception(f'unable to get last answer from list')
    
    new_nb_json = insert_cell(nb_index, answer_cell, nb_json,b_replace=b_replace)

    if len(new_nb_json.keys()) < 1:
        raise Exception('new_nb_json has no keys, not valid, not writing out')

    
    try:
        json.dump(new_nb_json, open(fn_nb,'w'))
    except Exception as e:
        raise Exception(f'unable to write to {fn_nb}, err: {e}')

    return 

