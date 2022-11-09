import sys
import compilation


if len(sys.argv) > 2:
    # maybe the user has specified multiple file names?
    print('you have specified too many arguments')
    sys.exit()

if len(sys.argv) < 2:
    # user hasn't specified a file name
    print('you need to specify the path to the file')
    sys.exit()

try:
    # get the source code
    file = open(sys.argv[1], 'r')
    contents = file.read()
    file.close()
    # compile it
    result = compilation.compile_to_js(contents)
    # get the file name and extension to name the out file
    [file_name, extension] = sys.argv[1].split('.', maxsplit=1)
    # to prevent removing the source file if it has the extension js
    out_file_name = f'{file_name}.js' if extension != 'js' else f'{file_name}_out.js'

    try:
        # write to the out file
        out_file = open(out_file_name, 'w+')
        out_file.write(result)
        out_file.close()
    except:
        print('file with the name ' + file_name + '.js already exists')

except FileNotFoundError:
    print('invalid file name')
