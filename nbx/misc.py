import subprocess
import time

try:
    from IPython.display import Javascript
    from IPython.display import display
except:
    print('unable to import from `IPython` package, this extension will not work')
    raise ImportError()

'''
    Module to hold one-off and deprecated code.

'''

# Deprecated ------------------------------------

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

def _leading_underscore_func():
    pass
    
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

# JS Functionality ----------------------

def demo_js():
    ''' 
         demo_js uses `display.display()` to execute a Javascript payload
    '''
    
    print('see devtools console for output')
    display(
        Javascript(data='console.log("demo_js");')
    )
    
def demo_js_to_python():
    ''' 
         a trick to get data in js into the python kernel the notebook
         is connected to
    '''
    
    js = '''
    IPython.notebook.kernel.execute("a=1");
    IPython.notebook.kernel.execute("print(f'the value of `a` is : {a}`");
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    display(Javascript(data=js))

# these are illustrative demo function connected to 
# JsToPythonScope.ipynb -------------------------------------------------------

def demo_js_scope_a():
    ''' 
         there's a tricky bug around getting the scope(?) correct to use the 
         newly set python variable within the js-calling module's method. 
            - once the input cell returns scope back to a notebook, 
                we can see the value has been set

         only after the full(?) cell has been run
    '''
    
    js = '''
    IPython.notebook.kernel.execute("a=99");
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    display(Javascript(data=js))

    return None

def demo_js_scope_b():
    ''' 
         set b to 99
    '''
    
    js = '''
    IPython.notebook.kernel.execute("b=99");
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    display(Javascript(data=js))

    return None

def demo_js_scope_d():
    ''' 
         set d to 99
    '''
    
    js = '''
    IPython.notebook.kernel.execute("d=99");
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    display(Javascript(data=js))

    return None

def demo_js_scope_e():
    ''' 
         set e to 99
         and run kernel.do_one_iteration()
    '''
    ip = get_ipython()
    
    ip.kernel.do_one_iteration()
    # ip.kernel.do_one_iteration()
    js = '''
    IPython.notebook.kernel.execute("e=99");
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    display(Javascript(data=js))

    ip.kernel.do_one_iteration()

    return None

def demo_js_scope_q():
    ''' 
         set d to 99
    '''
    
    js = '''
    IPython.notebook.kernel.execute("q.put(99)");
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    display(Javascript(data=js))

    return None

def demo_js_scope_c(val):
    ''' 
         set c to val
    '''
    
    js = f'''
    IPython.notebook.kernel.execute("c={val}");
    '''

    js = '\n'.join([line.strip() for line in js.split('\n') if line.strip !=''])
    
    display(Javascript(data=js))

    return None

def promise_pattern():
    '''
         show how to run code syncronously with promise pattern

         open devtools console before running, to see ~1 second delay
         before console outputs.
    '''    
    
    js = '''
    function demo() {
        function lots(){
            var x = 1;
            for (var i=0; i<1000000000; i++) {
                x += i
            }
        }
        Promise.resolve(
            lots()
            ).then(function(){
                return console.log('printing out with ~1 sec delay?')
                }
            );
        }
    demo();
    '''
    print('see devtools console for printout')
    display(Javascript(data=js))

def promise_set_print():
    '''
         doesnt work yet
         
         designed to show sync execution with messaging to python kernel

         works when function is called twice probably because biggie 
         has already been set at that point
    '''    
    
    js = '''
    
    var biggie = 0;
    
    function demo() {
        function lots(){
            var x = 1;
            for (var i=0; i<1000000000; i++) {
                x += i
            }
            biggie = x
        }
        Promise.resolve(
            lots()
            ).then(function(){
                return secondFunction();
                }
            ).then(function(){
                return thirdFunction();
                }
            );
            
            function secondFunction() {
                IPython.notebook.kernel.execute("a="+ biggie);
            }
            function thirdFunction() {
                  console.log('printing out with ~1 sec delay and setting a to bigges value')
            }
        }
    
    demo();
    '''
    
    display(Javascript(data=js))
    print('done')
    
    #These don't work right now, `a` only becomes available once we're back in notebook
    # global a
    # print([(k,v) for k,v in globals().items() if k == 'a'])
    # print(a)
    # print(f'the value of biggie (the variable `a` is this kernel) is: {a}')

def get_a():
    # doesnt work either
    global a
    print(a)
    