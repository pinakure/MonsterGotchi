from .position import Position

class Direction:
    NORTE       = 0
    NORDESTE    = 1
    ESTE        = 2
    SUDESTE     = 3
    SUR         = 4
    SUROESTE    = 5
    OESTE       = 6
    NOROESTE    = 7
    NAME        = {
        NORTE       : 'norte', 
        NORDESTE    : 'nordeste',
        ESTE        : 'este',
        SUDESTE     : 'sudeste',
        SUR         : 'sur',
        SUROESTE    : 'suroeste',
        OESTE       : 'oeste',
        NOROESTE    : 'noroeste'
    }
    INDEX        = {
        'norte'     : NORTE, 
        'nordeste'  : NORDESTE,
        'este'      : ESTE,
        'sudeste'   : SUDESTE,
        'sur'       : SUR,
        'suroeste'  : SUROESTE,
        'oeste'     : OESTE,
        'noroeste'  : NOROESTE
    }
    DELTA        = {        
        NORTE       : Position( 0,-1), 
        NORDESTE    : Position( 1,-1),
        ESTE        : Position( 1, 0),
        SUDESTE     : Position( 1, 1),
        SUR         : Position( 0, 1),
        SUROESTE    : Position(-1, 1),
        OESTE       : Position(-1, 0),
        NOROESTE    : Position(-1,-1)
    }