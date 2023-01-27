from typeguard import typechecked

@typechecked
def lighten(color: str, value: int = 20)-> str :
    """
    Ligthen an hexa color

    Parameters
    ----------
    color : str
        color to lighten in hex
    value : int
        the value to add on red, green and blue composants
    
    Returns 
    ---------
    string : 
        the lightened color in hex
    """
    r = value + (int(color[1:3], 16))
    g =  value +(int(color[3:5], 16))
    b = value +  (int(color[5:7], 16))
    if r>255 :
        r=255
    if g>255 :
        g=255
    if b>255 :
        b=255

    rh = str(hex(int(r)))[2:4]
    gh = str(hex(int(g)))[2:4]
    bh = str(hex(int(b)))[2:4]

    if len(rh) <2 :
        rh = "0" + rh
    if len(gh) <2 :
        gh = "0" + gh
    if len(bh) <2 :
        bh = "0" + bh

    return('#' + rh + gh + bh)


