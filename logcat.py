#!/usr/bin/env python2.6
# coding: utf-8


import os, sys
import stat
import time
import errno
import logging

I_INODE = 0
I_SIZE = 1
I_OFFSET = 2

NODATA_WAIT_SECONDS = 3
NODATA_CHECK_INTERVAL = 1
NODATA_TICKS = NODATA_WAIT_SECONDS / NODATA_CHECK_INTERVAL


STAT_DIR = '/tmp'


def fsize( f ):
    st = os.fstat( f.fileno() )
    return st[ stat.ST_SIZE ]


def dumb_logger():
    l = logging.Logger( '_dumb_' )
    l.setLevel( logging.CRITICAL )
    return l


class Cat( object ):

    default = {
            'preprocess' : lambda l: None if l.strip() == '' else l.strip(),
            'exclusive'  : True,
            'log'        : dumb_logger(),
            'id'         : os.path.split( sys.argv[0] )[ -1 ],
            'strip'      : False,
    }


    def __init__( self, fn, **ctx ):

        self.fn = fn
        self.ctx = ctx
        self.running = None

        for k, v in Cat.default.items():
            self.ctx.setdefault( k, v )

        self.log = self.ctx[ 'log' ]

        if type( self.ctx[ 'handler' ] ) == type( [] ):
            self.handlers = self.ctx[ 'handler' ]
        else:
            self.handlers = [ self.ctx[ 'handler' ] ]

        self.handlers = [ ( x if callable( x ) else x.handle )
                          for x in self.handlers ]


    def cat( self ):
        self.running = True
        try:
            self._cat()
        finally:
            self.running = False

    def get_handler( self ):
        return self.ctx[ 'handler' ]

    def stat_fn( self, f ):
        return os.path.join( STAT_DIR, self.stat_key( f ) )


    def stat_key( self, f ):
        name = os.path.realpath( f.name )
        name = 'logcat_stat_!' + self.ctx[ 'id' ] + '!'.join( name.split( '/' ) )
        return name


    def lock_name( self, fn ):
        name = os.path.realpath( fn )
        name = 'logcat_lock_!' + self.ctx[ 'id' ] + '!'.join( name.split( '/' ) )
        return name


    def read_last( self, f ):

        with open( self.stat_fn( f ) ) as stf:
            _last = stf.read( 1024 )

        last = _last.strip().split( ' ' )
        if len( last ) != 3:
            raise IOError( 'InvalidRecordFormat', _last )

        ( lastino, lastsize, lastoff ) = last

        lastino = int( lastino )
        lastsize = int( lastsize )
        lastoff = int( lastoff )

        return ( lastino, lastsize, lastoff )


    def write_last( self, f ):

        st = os.fstat( f.fileno() )

        ino = st[ stat.ST_INO ]
        offset = f.tell()

        # record offset as size because size would change after the last scan
        size = offset

        with open( self.stat_fn( f ), 'w' ) as stf:
            stf.write( '%d %d %d' % ( ino, size, offset ) )

        self.log.info( 'position written fn=%s inode=%d size=%d offset=%d' % (
                self.fn, ino, size, offset ) )

    def is_changed( self, f ):

        st = os.fstat( f.fileno() )
        ino = st[ stat.ST_INO ]
        size = st[ stat.ST_SIZE ]

        try:
            last = self.read_last( f )
            if last[ I_INODE ] == ino and last[ I_SIZE ] <= size and last[ I_OFFSET ] <= size:
                return False
            return True
        except IOError, e:
            # no such file
            return True


    def get_last_offset( self, f ):

        if self.is_changed( f ):
            return 0
        else:
            last = self.read_last( f )
            return last[ 2 ]


    def wait_for_new_data( self, f ):

        for ii in range( NODATA_TICKS ):

            if f.tell() < fsize( f ):
                return True
            else:
                time.sleep( NODATA_CHECK_INTERVAL )

        return False


    def cat_to_end( self ):

        fn = self.fn

        size1read = 1024 * 1024 * 64

        with open( fn ) as f:
            self.log.info( 'file opened: ' + fn )

            offset = self.get_last_offset( f )
            f.seek( offset )

            self.log.info( 'scan at offset: ' + str( offset ) )

            while self.wait_for_new_data( f ):

                while f.tell() < fsize( f ):

                    lines = f.readlines( size1read )

                    for line in lines:
                        if self.ctx[ 'strip' ]:
                            line = line.strip('\r\n')

                        for h in self.handlers:
                            try:
                                h( line )
                            except Exception, e:
                                pass

                    self.write_last( f )

                    for ii in range( 3 ):
                        if fsize( f ) - f.tell() > size1read:
                            break
                        else:
                            time.sleep( 1 )


    def _nolock_cat( self ):

        self.wait_for_file()

        while True:

            try:
                self.cat_to_end()

            except IOError, e:

                if e[ 0 ] != errno.ENOENT:
                    raise

                while not os.path.isfile( self.fn ):
                    time.sleep( 10 )

            # quit if no more data. wait a little while
            time.sleep( 5 )

    def wait_for_file( self, timeout=3600 ):

        t0 = int(time.time())

        while True:
            try:
                open( self.fn )
                return
            except IOError as e:

                if e[ 0 ] != errno.ENOENT:
                    raise

                if int( time.time() ) - t0 > timeout:
                    self.log.warn( repr( e ) + ' while waiting for %s' % ( self.fn, ) )

                    # warn only once
                    timeout = 86400 * 365

                self.log.info( repr( e ) + ' while waiting for %s' % self.fn )
                time.sleep( 10 )


    def _cat( self ):

        if self.ctx[ 'exclusive' ]:

            # TODO add lock
            self._nolock_cat()

        else:
            self._nolock_cat()


def echo( line ):
    print line

if __name__ == "__main__":

    ctx = {
            'handler': echo,
    }

    fn = '/var/log/cron'

    c = Cat( fn, **ctx )
    c.cat()
