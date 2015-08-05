import sys

def linesplit( filename ):

    with open( filename, 'r' ) as inputfile:

        buf = ''
        while True:

            chunck = inputfile.read( 1024*32 )
            if chunck == '':
                break

            buf += chunck

            lines = buf.split( ')' )
            buf = lines[ -1 ]

            for line in lines[ :-1 ]:
                if '(' in line:
                    yield line.split( '(', 1 )[ 1 ]

for line in linesplit( sys.argv[1] ):
    print '(' + line + ')'
