def very_important_function(file, template, *variables, file_path="/dev/null", engine, header = True, debug = False, verbose = False):
    """Does something to `file` that's very important"""
    with open(file, 'w') as f:
        print(f.read())
    
    j=23+45
    i       = 12
    return j/i
