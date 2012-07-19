#!/usr/bin/env python

# DirPyLint - A program to analyze directories based on qualifications specified in a config file
# Copyright (C) 2012 William Farmer
                                     
import os
import sys
import yaml
import time
import re
import optparse

error_count = 0

log    = open('dirpylint.log', mode='w')
report = open('report.txt', mode='w')

def main():

    print '***************************************************'
    print 'DirPyLint Copyright (C) 2012 William Farmer'
    print 'This program comes with ABSOLUTELY NO WARRANTY;'
    print 'for details, see the LICENSE file included.'
    print 'This is free software, and you are welcome to'
    print 'redistribute it under certain conditions;'
    print 'for details, see the LICENSE file included.'
    print '***************************************************'

    opts        = get_args()
    try:
        config_file = open(opts.config, mode='r')
        config      = yaml.load(config_file)
    except IOError:
        print 'BAD CONFIG FILE -- QUITTING'
        sys.exit(1)

    start_time = time.time()

    global error_count
    global log
    global report

    return_code = 0

    for level in range(config['levels']):
        log.write('***************************************************\n')
        log.write('level %i\n'%level)
        log.write('***************************************************\n')
        report.write('***************************************************\n')
        report.write('LEVEL %i\n'%level)
        report.write('***************************************************\n')
        final_score = LevelScan(level, config)
        return_code += final_score

    report.write('***************************************************\n')
    report.write('Final Score = %i'%error_count)
    print 'RETURN CODE = %i'%return_code
    end_time     = time.time()
    elapsed_time = end_time - start_time
    print 'Elapsed Time = %s'%elapsed_time

def LevelScan(level, config):

    dir_needs       = config['level%s'%level]['dirs']['needs']
    dir_optional    = config['level%s'%level]['dirs']['optional']
    dir_not         = config['level%s'%level]['dirs']['not']
    dir_ignore      = config['level%s'%level]['dirs']['ignore']
    file_types      = config['level%s'%level]['files']['types']
    file_needs      = config['level%s'%level]['files']['needs']
    file_optional   = config['level%s'%level]['files']['optional']
    file_not        = config['level%s'%level]['files']['not']
    file_ignore     = config['level%s'%level]['files']['ignore']
    dir_expression  = config['level%s'%level]['dirs']['regex']
    file_expression = config['level%s'%level]['files']['regex']
    ignore_tree     = config['ignore_tree']

    dir_score       = dirs_scan(config, level, dir_needs, dir_optional, dir_not, dir_ignore, ignore_tree)
    file_score      = file_scan(config, level, file_types, file_needs, file_optional, file_not, file_ignore, ignore_tree)
    regex_score     = regex_match(config, level, dir_expression, file_expression, dir_ignore, file_ignore, ignore_tree)
    final_score     = dir_score + file_score + regex_score
    return final_score
    

def regex_match(config, level, dir_expression, file_expression, dir_ignore, file_ignore, ignore_tree):
    
    global error_count
    global log
    global report

    directory_scan  = os.walk(config['root'])
    flag            = False

    if dir_expression != False:
        for path, dirs, files in directory_scan:
            for item in dirs:
                if item in dir_ignore:
                    pass
                elif re.match(dir_expression, item) == None:
                    directory_path = os.path.join(path, item)
                    for ignored in ignore_tree:
                        if ignored != False:
                            if directory_path.startswith(ignored) == False:
                                report.write('regex directory error = %s  %s\n'%(dir_expression, directory_path))
                                error_count += 1
                                flag = True
                        elif ignored == False:
                            report.write('regex directory error = %s  %s\n'%(dir_expression, directory_path))
                            error_count += 1
                            flag = True


    file_scan  = os.walk(config['root'])

    if file_expression != False:
        for path, dirs, files in file_scan:
            for item in files:
                if item in file_ignore:
                    pass
                elif re.match(file_expression, item) == None:
                    file_path = os.path.join(path, item)
                    for ignored in ignore_tree:
                        if ignored != False:
                            if directory_path.startswith(ignored) == False:
                                report.write('regex file error = %s  %s\n'%(file_expression, file_path))
                                error_count += 1
                                flag = True
                        elif ignored == False:
                            report.write('regex file error = %s  %s\n'%(file_expression, file_path))
                            error_count += 1
                            flag = True
    if flag:
        return 1
    else:
        return 0

def file_scan(config, level, file_types, file_needs, file_optional, file_not, file_ignore, ignore_tree):
    
    global error_count
    global log
    global report


    directory_scan = os.walk(config['root'])
    flag           = False

    for path, dirs, files in directory_scan:
        if Leveler(level, path, config['root'], ignore_tree):
            for scan_file in files:
                for Ftype in file_types:
                    if Ftype == False:
                        pass
                    elif (scan_file.endswith(Ftype) == True) and (scan_file not in file_ignore):
                        report.write('unsupported file type = %s\n'%os.path.join(path,scan_file))
                        error_count += 1
                        flag = True
            for item in file_needs:
                if item not in files:
                    report.write('need file             = %s\n'%os.path.join(path, item))
                    error_count += 1
                    flag = True
    if flag:
        return 1
    else:
        return 0

def dirs_scan(config, level, dir_needs, dir_optional, dir_not, dir_ignore, ignore_tree):
    
    global error_count
    global log
    global report

    directory_scan = os.walk(config['root'])
    flag           = False

    for path, dirs, files in directory_scan:
            if Leveler(level, path, config['root'], ignore_tree):
                if (dirs in dir_ignore):
                    pass
                else:
                    for item in dir_needs:
                        if (item not in dirs) and (item != False):
                            report.write('need directory        = %s\n'%os.path.join(path, item))
                            error_count += 1
                            flag = True
                    for item in dir_not: 
                        if item in dirs:
                            report.write('not directory         = %s\n'%os.path.join(path, item))
                            error_count += 1
                            flag = True
                    for item in dirs:
                        if (item not in dir_needs) and (item not in dir_not) and (item not in dir_optional) and (item not in dir_ignore):
                            report.write('unexpected directory  = %s\n'%os.path.join(path, item))
                            flag = True
    if flag:
        return 1
    else:
        return 0

def Leveler(level, path, root, ignore_tree):

    assert(path.startswith('/'))
    assert(root.startswith('/'))

    slash_count = 0
    for byte in path[len(root):]:
        if byte == '/':
            slash_count += 1

    log.write('full path   = %s\n'%path)
    log.write('file path   = %s\n'%path[len(root):])
    log.write('level count = %i\n'%slash_count)
    for item in ignore_tree:
        if path.startswith(item):
            return False
    if slash_count == level:
        return True
    else:
        return False

def get_args():
    global opts
    global args
    parser = optparse.OptionParser(usage = 'UsageL %prog <options>', version = 'Version 1.0')
    parser.add_option('-c', '--config', action='store', type='string', default='./config.yaml', help='Where is the config file located')
    opts, args = parser.parse_args()

    return opts

if __name__ == "__main__":
    sys.exit(main())
