/*
    template scripts for calls to browser
*/


//template for flash animation
function flash(ms_flash) {
Promise.resolve(
    $(html_cell).stop().animate({backgroundColor:'#008000'}, ms_flash).promise()
    ).then(function(){
        return $(html_cell).stop().animate(
            {backgroundColor:'#FFFFFF'}, ms_flash);
        }
    );
}


// This show a 1-second delay from call to printout
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
            return console.log('done')
            }
        );
    }

/* 
    The following shows that we're truly executing async
    with the simple promise pattern for save_notebook

    in static/notebook/js/notebook/js/notebook.js 
        line <2842>
        <within save_notebook_success()>
        ->set a breakpoint

    compare performance of off() vs "two liner" below:

        off(): console doesn't print when debugger stops
        two liner: console has printed

    off2() shows that we need to continue the .then nesting
    to keep the synchronous method
*/

//Synchronous execution: log doesn't occur before breakpoint
function off() {
    Promise.resolve(
        IPython.notebook.save_notebook(true)
        ).then(function(){
            return console.log('done')
            }
        );
    }

//ASyncronous: log occurs before breakpoint is hit
IPython.notebook.save_notebook();
console.log('done');

//Sync And Async: 'really done' prints out async
function off2() {
    Promise.resolve(
        IPython.notebook.save_notebook(true)
        ).then(function(){
            return console.log('done')
            }
        );
    console.log('really done')
    }

//Complete Asnyc
//note: afinally() is defined below it's invocation yet still works
function off3() {
    
    Promise.resolve(
        IPython.notebook.save_notebook(true)
        ).then(function(){
            return console.log('done')
            }
        ).then(function() {
            return afinally();
            }
        );
    function afinally() {console.log('really done');}
    }
    
