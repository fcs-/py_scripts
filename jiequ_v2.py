#coding: utf-8
import sys

def linesplit( filename ):
    """按字节读取文件
    """

    with open( filename, 'r' ) as inputfile:

        buf = ''
        while True:

            # 合理设置单次读取大小，可以提高读取速度
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
