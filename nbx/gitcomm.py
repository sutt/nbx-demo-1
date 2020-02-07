import os, sys
import time
import subprocess

'''
gitcomm - module for callings commands to git for inter-machine communication

TODOs
[ ] git status between each command
[ ] find_root_git()
[ ] does pull_answer() work?

'''

CELLS_DIR = '.nbx'
CELLS_JSON = os.path.join(CELLS_DIR, 'master.json')

def cmd_line_strip(cmd):
    ''' 
         return list of strings: - one per line of command string 
                                 - without indents 
                                 - remove blank lines
         
         note: might not work with tabs, and some editors might insert those
               in the python code file.
    '''
    return [line.strip() for line in cmd.split('\n') 
            if any([e != '' for e in line.strip().split(' ')])
            ]

def cmd_words_sep(list_lines):
    ''' 
         return each separate word in cmd-string as an item within a list

         note: this doesn't work for `--flag=value` (where there are no spaces)

         note: this separates separate words in the commit message
    '''
    return [[e for e in line.split(' ') if e != ''] for line in list_lines]

def cmd_adj(cmd):
    '''
        prepare [multi-line] cmd string for use in subprocess call:

        return a list of list of strings, e.g.:

             [['git', 'add', '.'], ['git', 'status']]
             or
             [['ls', '-a']]
    '''
    return cmd_words_sep(cmd_line_strip(cmd))


def find_root_git():
    ''' return relative path to root of git repo '''
    pass
    #TODO

def push_answer(remote_name='origin', b_log=False):
    '''
         run `git add, commit, push` 

         only on .nbx/master.json

         note: commit message must have no spaces right now
    '''
    cmd = f'''
    git add {CELLS_JSON}
    git commit -m 'push-answer-script'
    git push {remote_name} master
    git status
    '''
    
    list_list_cmd = cmd_adj(cmd)
    
    t0 = time.time()
    output = ''
    for list_cmd in list_list_cmd:
        
        output += f'\n ------------------------------------------------------\n'
        output += ' '.join(list_cmd)
        output += f'\n ------------------------------------------------------\n'
        
        output_ret = subprocess.check_output(list_cmd)

        try:
            output_utf8 = output_ret.decode('utf-8')
            output += output_utf8
        except Exception as e:
            output += 'Error: failed to decode output\n'
            print(f'Error: failed to convert check_output return text as utf-8: {e}')
    
    cmd_time = time.time() - t0

    if b_log:
        print(f'time for check_output: {round(cmd_time,2)}')
        print('======================Output===========================')
        print(output)
            


def pull_answer(remote_name='origin', b_log=False):
    '''
         run `git pull`
    '''

    cmd = f'''
    git pull {remote_name} master
    '''
    
    list_list_cmd = cmd_adj(cmd)
    
    t0 = time.time()
    output = ''
    for list_cmd in list_list_cmd:
        
        output += f'\n ------------------------------------------------------\n'
        output += ' '.join(list_cmd)
        output += f'\n ------------------------------------------------------\n'
        
        output_ret = subprocess.check_output(list_cmd)

        try:
            output_utf8 = output_ret.decode('utf-8')
            output += output_utf8
        except Exception as e:
            output += 'Error: failed to decode output\n'
            print(f'Error: failed to convert check_output return text as utf-8: {e}')
    
    cmd_time = time.time() - t0

    if b_log:
        print(f'time for check_output: {round(cmd_time,2)}')
        print('======================Output===========================')
        print(output)
