#! /usr/bin/env python
import os
import re
import shutil
from os.path import splitext

SOURCE = os.getcwd() + "/www/"
TARGET = os.getcwd() + "/compiled/"

ECHO_VAR_TEMPLATE = '<!--#echo var="%s"-->'
SET_VAR_VALUE_TEMPLATE = '<!--#set var="%s" value="%s"-->'
SET_VAR_VALUE_REGEXP = r'<!--#set var="([^"]*)" value="([^"]*)"-->'
INCLUDE_VIRTUAL_TEMPLATE = '<!--#include virtual="%s" -->'
INCLUDE_VIRTUAL_REGEXP = r'<!--#include virtual="([^"]*)" -->'

if not os.path.exists(TARGET):
    os.makedirs(TARGET)

def include_files(filename):
    content = open(filename).read()
    include_regexp = re.compile(INCLUDE_VIRTUAL_REGEXP)
    for file in include_regexp.findall(content):
        abs_filename = "%s%s" % (SOURCE, file)
        abs_filename = abs_filename.replace('//', '/')
        include_content = include_files(abs_filename)
        content = content.replace(INCLUDE_VIRTUAL_TEMPLATE % file, include_content)
    return content
    
def replace_variables(content):
    processed = content
    set_var_regex = re.compile(SET_VAR_VALUE_REGEXP)
    for key, value in set_var_regex.findall(content):
        # Replace variables with values.
        processed = processed.replace(ECHO_VAR_TEMPLATE % key, value)
        # Remove variables initializations.
        processed = processed.replace(SET_VAR_VALUE_TEMPLATE % (key, value), "")
    return processed

def compile_files():
    print("Compiling files from:")
    print(SOURCE)
    print("To")
    print(TARGET)
    for root, dirs, files in os.walk(SOURCE):
        for file in files:
            source_file = os.path.join(os.path.abspath(root), file)
            relative_path = source_file.replace(SOURCE, "")
            target_file = os.path.join("%s%s" % (TARGET, relative_path))
            f, extension = os.path.splitext(file)
            print 'Next...'
            if extension == ".shtml":
                print("From file %s" % source_file)
                target_file = target_file.replace('.shtml', '.html')
                compiled_content = include_files(source_file)
                compiled_content = replace_variables(compiled_content)
                f = open(target_file, 'w')
                f.write(compiled_content)
                f.close()
                print("Compile to %s" % target_file)
            else:
                print("Copy %s" % source_file)
                shutil.copy(source_file, target_file)
                print("To %s" % target_file)

confirm = raw_input("We will compile shtml project to html. Type yes to continue.\n")
if confirm == u'yes':
    compile_files()
else:
    print("Abort.")
