import subprocess

try:
    from IPython.display import Javascript
    from IPython.display import display
except:
    print('unable to import from `IPython` package, this extension will note work')
    raise ImportError()

# Documentation + Tips ---------------
'''
TODOS

[x] save functionality
[ ] laod js from templates
    -> a separate file for each js function?
    -> how to set flag variables in python string?

Documentation & Tips:

+ getting notebooks in <root>/misc/book to import <root>/cpr:

import sys
sys.path.append('../../')
from IPython import display
from IPython.display import Javascript
%reload_ext autoreload
%autoreload 2
import cpr.cpr as cpr

'''


    
def set_nbname_global():
    '''
         set NBX_NBNAME_GLOBAL to the string of the notebook's name

         this will only occur/ be available to python kernel after all 
         input code has run and the cell's output has returned.

         call this on module load to set nbname for future functions default
    '''
    
    js = '''
    var nbName = IPython.notebook.notebook_name;
    var cmd = "NBX_NBNAME_GLOBAL = '" + nbName + "'";
    IPython.notebook.kernel.execute(cmd);
    console.log(cmd);
    '''
    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    display(Javascript(data=js))
    
    

def reload_nb(  b_save=False,
                b_scroll=True,
                b_select=True,
                b_flash=True,
                b_log=True,
                debug=False,
                ):
    '''
         reload-notebook + goto-cell via javascript

         b_ variables - control different behaviors
         debug        - if True, output string of js commands to file

         note: do not print js to notebook which creates a loop
               
    '''
    
    
    def js_bool(py_bool):
        if py_bool: return 'true'
        return 'false'

    js = f'''
    var b_save = {js_bool(b_save)};
    var b_scroll = {js_bool(b_scroll)};
    var b_select = {js_bool(b_select)};
    var b_flash = {js_bool(b_flash)};
    var b_log = {js_bool(b_log)};
    '''


    js += '''
    
    var nb_path = IPython.notebook.notebook_path;
    var cell_index = IPython.notebook.get_selected_index() - 1;
    
    if (b_log) {console.log('selected_index: ' + cell_index);}

    //save notebook waits for finish
    if (b_save) {
        Promise.resolve(
        IPython.notebook.save_notebook(true)
        ).then(function(){
            // this is where we'll call to python kernel
            return console.log('done with save')
            }
        ).then(function() {
            return theRest();
            }
        );

    } else {
        theRest();
    }
    
    function theRest() {

    IPython.notebook.load_notebook(nb_path);
    
    if (b_log) {console.log('after load');}
    
    setTimeout(basicFunc, 500);
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
    
    if (b_log) {console.log('end of js payload');}
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    if debug:
        try:
            with open('assets/js-debug.js', 'w') as f:
                f.write(js)
        except:
            print('debug option set True, but failed to output js to `assets/js-debug.js. directory might not exist?')

    display(Javascript(js))
    