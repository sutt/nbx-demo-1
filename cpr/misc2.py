import os, sys, time
from IPython.display import display, Javascript


'''
    Demo functions: how to write everything in js, and do
    python via kernel.execute

    This allows await for async js functions
    and communication between js-kernel and python-kernel
'''

def demo_save(debug=False):
    ''' should show `my_time` ~ 88 in python kernel
        because it takes some time to execute notebook_save
    '''
    
    js = '''
    var date0 = new Date();
    var t0 = date0.getTime();
    var py_cmd = '';
    py_cmd += 'my_time = ';
    
    Promise.resolve(
        IPython.notebook.save_notebook(true)
        ).then(function(){
            return theFinal();
            }
        );

    function theFinal() {
        var date1 = new Date();
        var t1 = date1.getTime();
        var tDiff = t1 - t0;
        py_cmd += tDiff.toString();
        console.log(tDiff);
        IPython.notebook.kernel.execute(py_cmd);
        }
    '''
    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    if debug:
        try:
            with open('assets/js-debug-misc2.js', 'w') as f:
                f.write(js)
        except:
            print('debug option set True, but failed to output js to `assets/js-debug.js. directory might not exist?')

    display(Javascript(js))


def demo_nosave(debug=False):
    ''' should show `my_time` ~ 1 in python kernel
        because it takes almost no time to execute 
        because we didn't call notebook_save() as we 
        do in demo_save().
    '''
    
    js = '''
    var date0 = new Date();
    var t0 = date0.getTime();
    var py_cmd = '';
    py_cmd += 'my_time = ';
    
    Promise.resolve(
        //IPython.notebook.save_notebook(true)
        1+1
        ).then(function(){
            return theFinal();
            }
        );

    function theFinal() {
        var date1 = new Date();
        var t1 = date1.getTime();
        var tDiff = t1 - t0;
        py_cmd += tDiff.toString();
        console.log(tDiff);
        IPython.notebook.kernel.execute(py_cmd);
        }
    '''
    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    if debug:
        try:
            with open('assets/js-debug-misc2.js', 'w') as f:
                f.write(js)
        except:
            print('debug option set True, but failed to output js to `assets/js-debug.js. directory might not exist?')

    display(Javascript(js))
