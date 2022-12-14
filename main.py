import sys
import compilation


if len(sys.argv) < 2:
    # user hasn't specified a file name
    print('you need to specify the path to the file')
    exit()

for arg in sys.argv[1:]:
    # iterate through each file submitted for compilation
    try:
        # get the source code
        file = open(arg, 'r')
        contents = file.read()
        file.close()

        # get the file name and extension to name the out file
        # reversed to ensure that only the file extension is removed
        [extension, file_name] = arg[::-1].split('.', maxsplit=1)
        file_name = file_name[::-1]  # [::-1] reverses the string
        extension = extension[::-1]

        # compile the code
        print(f"compiling '{arg}'")
        result = compilation.compile_to_js(contents)
        # don't write output if compilation fails
        # instead skip this file
        if result == None:
            continue

        out_file_name = file_name + ('.js' if extension != 'js' else '_out.js')

        with open(out_file_name, 'w+') as out_file:
            out_file.write(result)
            out_file.close()

        print(f"compiled '{arg}' to {out_file_name}")

    except FileNotFoundError:
        print(f"could find '{arg}'")
