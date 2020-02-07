import os, sys, time
from IPython.display import display, Javascript

from .merge import get_answer
from .merge import give_answer

from .frontend import reload_nb

from .gitcomm import pull_answer
from .gitcomm import push_answer

from .utils import get_nb_name

'''
     Module for v2 functionality on nbx. Additons include:

        - save before send/receive
        - can conceivably solve issues:
            - multi notebook
            - multi cell containing target text
            - notebook not at root of git
            - notebook not at root of jupyter server

    These methods are wrapped completely in js 
    and execute python only thru js-call to Ipyuthon kernel 
    so they are more difficult to code / work with in IDE.

'''

class ImportClass:

    '''
         a helper method for calling methods from other modules in js
    '''

    def __init__(self):
        pass

    @staticmethod
    def merge_give_answer(fn_nb):
        give_answer(fn_nb=fn_nb,term='send_answer')

    @staticmethod
    def gitcomm_push_answer():
        push_answer()

    @staticmethod
    def gitcomm_pull_answer():
        pull_answer(remote_name='local', 
                b_log=False,
                )
    
    @staticmethod
    def merge_get_answer(fn_nb):
        get_answer( fn_nb=fn_nb, 
                    term='receive_answer',
                    b_replace=False,
                    )
    
    @staticmethod
    def cpr_reload_nb():
        reload_nb(  b_save=False, 
                    b_scroll=True,
                    b_flash=True,
                    b_select=True,
                    b_log=False,
                    debug=False,
                    )


def receive_answer( debug=False,):
    '''
         like `nbx.receive_answer` but:
            - all in js
            - less arguments / options
    '''

    js = '''
    Promise.resolve(
        IPython.notebook.save_notebook(true)
        ).then(function(){
            return theFinal();
            }
        ).then(function(){
            return theRest();
        });

    function theFinal() {
        
        var nb_name = IPython.notebook.notebook_name;
        
        var py_cmd = '';
        py_cmd += 'nbx2.ImportClass.gitcomm_pull_answer()';
        IPython.notebook.kernel.execute(py_cmd);
        console.log(py_cmd);

        var py_cmd = '';
        py_cmd += 'nbx2.ImportClass.merge_get_answer("' + nb_name + '")';
        IPython.notebook.kernel.execute(py_cmd);
        console.log(py_cmd);

        }

    function theRest() {

    
    var nb_path = IPython.notebook.notebook_path;
    var cell_index = IPython.notebook.get_selected_index() - 1;

    var b_log = true;
    var b_save = false;
    var b_scroll = true;
    var b_select = true;
    var b_flash = true;

    
    setTimeout(loadFunc, 500);
    function loadFunc() {
    IPython.notebook.load_notebook(nb_path);
    }
    if (b_log) {console.log('after load');}
    
    setTimeout(basicFunc, 700);
    function basicFunc() {
        
        console.log('in basicFunc');   
        var orig_cell = IPython.notebook.get_cell(cell_index);
        var html_cell = $(orig_cell.element)[0];
        
        if (b_scroll) {
        $(orig_cell.element)[0].scrollIntoViewIfNeeded({inline:'center'});}
        
        if (b_select) {IPython.notebook.select(cell_index);}
        
        function flash(ms_flash) {
            Promise.resolve(
                $(html_cell).stop().animate({backgroundColor:'#008000'}, ms_flash).promise()
                ).then(function(){
                    return $(html_cell).stop().animate(
                        {backgroundColor:'#FFFFFF'}, ms_flash);
                    }
                );
        }
        if (b_flash) {flash(500);}
        
        if (b_log) {console.log('end of basicFunc')}
    } // end basicFunc ------------
    
    if (b_log) {console.log('done with theRest()');}
    } // end theRest---------------
    
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    if debug:
        try:
            with open('js-debug-nbx2.js', 'w') as f:
                f.write(js)
        except:
            print('debug option set True, but failed to output js to `js-debug.js. directory might not exist?')

    display(Javascript(js))




def send_answer( debug=False,):
    '''
         like `nbx.send_answer` but:
            - all in js
            - less arguments / options
    '''

    
    js = '''
    Promise.resolve(
        IPython.notebook.save_notebook(true)
        ).then(function(){
            return theFinal();
            }
        );

    function theFinal() {
        
        var nb_name = IPython.notebook.notebook_name;
        
        var py_cmd = '';
        py_cmd += 'nbx2.ImportClass.merge_give_answer("' + nb_name + '")';
        
        IPython.notebook.kernel.execute(py_cmd);
        console.log(py_cmd);

        var py_cmd = '';
        py_cmd += 'nbx2.ImportClass.gitcomm_push_answer()';

        IPython.notebook.kernel.execute(py_cmd);
        console.log(py_cmd);

        }
    '''
    
    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    if debug:
        try:
            with open('js-debug-nbx2.js', 'w') as f:
                f.write(js)
        except:
            print('debug option set True, but failed to output js to `js-debug.js. directory might not exist?')

    display(Javascript(js))

    print('send_answer done.')