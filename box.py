'''
Parametric Scifi Boxes
author: Adrian Herbez (zanzastoys)

This will create a 3d printable, stackable container suitable
for scifi dioramas. The sizes are tuned to work well with 1:18
scale action figures.

It is recommended that you reserve changes to just the
height, width, and depth variables, but feel free to experiment.

Enjoy! And if you find value in this, please consider subscribing
to our youtube channel: https://www.youtube.com/@zanzastoys
'''

import cadquery as cq
import math

# base dimensions for the main box, not including
# the side panels and reinforcing rings
height = 30.0
width = 40.0
depth = 25.0

# change this to make the box more or less round
baseFillet = 5

topHeight = baseFillet + 1

lip = 2.6

# these control the cutout on the side
handleW = 10
handleH = 5

sidePanelThick = 1.2;

clearance = 0.4

def ring(w, d, h, t):
    ring = cq.Workplane("XY").box(w, d, h)
    ring = ring.edges("|Z").fillet(4)
    
    inner = cq.Workplane("XY").box(w - (t*2), d - (t*2), h*2)
    inner = inner.edges("|Z").fillet(4-t)
    
    ring = ring.cut(inner)

    return ring

def sidePanel(startWidth, startDepth):
    w = startWidth - (baseFillet*2)
    #d = depth - (baseFillet*2)
    h = height - topHeight + lip
    t = sidePanelThick
    d = startDepth + (sidePanelThick*2)
    
    panel = cq.Workplane("XZ").box(w, h, t+ 0.1)
    
    panel = cq.Workplane("XZ").box(w, h, d)
    
    pts = [
        (-handleW/2, h / 2.0 + 0.1),
        ( handleW/2, h / 2.0 + 0.1),
        ( handleW/2 * 0.8, (h / 2.0 - handleH)),
        (-handleW/2 * 0.8, (h / 2.0 - handleH)),
    ]

    cutout = cq.Workplane("XZ").polyline(pts).close().extrude(d*2)
    cutout = cutout.edges("|Y and <Z").fillet(1)
    cutout = cutout.translate([0, d, 0])
    
    cutout = cutout.translate([0,5,0])
    cutout2 = cutout.mirror(mirrorPlane="XY")
    
    cutout3 = cq.Workplane("XZ").box(
        w - (6.4),
        h - (handleH*2) - (3.2),
        d*2
        )
    cutout3 = cutout3.edges("|Y").fillet(1)
    
    panel = panel.cut(cutout)
    panel = panel.cut(cutout2)
    panel = panel.cut(cutout3)
    
    panel = panel.edges("|Y and >Z").fillet(0.8)
    panel = panel.edges("<Y or >Y").fillet(0.6)
    
    panel = panel.translate([0,0,h/2])
    
    return panel

def bottom():
    
    w = width - (baseFillet*2)
    d = depth - (baseFillet*2)
    h = height - topHeight - lip
    
    f = baseFillet
    wall = 1.6
    
    b = cq.Workplane("XY").box(width, depth, h)
    b = b.edges("|Z or <Z").fillet(f)
    b = b.translate([0,0,h/2 + lip])
    
    raiser = h/2 + lip

    s = sides()
    b = b.union(s)

    inner = cq.Workplane("XY").box(width-3.2, depth - (wall*2), h*2)
    inner = inner.edges("|Z or <Z").fillet(f - 1.6)
    inner = inner.translate([0,0,1.6])
    inner = inner.translate([0,0,h + lip])
    
    # r = ring(w + baseFillet, d + baseFillet, lip*2, 1.2)
    # show_object(r) 
    # show_object(b)
    
    rw = w + baseFillet
    rd = d + baseFillet
    rh = lip * 2
    t = 1.2

    rOuter = cq.Workplane("XY").box(rw, rd, rh)
    rOuter = rOuter.edges("|Z").fillet(4)
    rOuter = rOuter.translate([0, 0, (rh/2)])
    
    rInner = cq.Workplane("XY").box(rw - (t*2), rd - (t*2), lip*2)
    rInner = rInner.edges("|Z").fillet(4-1.2)
    # rInner = rInner.translate([0, 0, -(h/2) + raiser])
    
    sw = width - (wall * 2)
    sd = depth - (wall * 2)
    sh = topHeight
    
    if (width < depth):
        sw += (wall * 4)
    else:
        sd += (wall * 4)
    
    slot = cq.Workplane("XZ").box(sw, sh, sd)
    slot = slot.translate([0, 0, h + (sh/2)+lip])
    
    b = b.union(rOuter)
    b = b.cut(inner)
    b = b.cut(rInner)
    b = b.cut(slot)
    
    
    return b

def top():
    w = width - (baseFillet*2)
    d = depth - (baseFillet*2)
    h = topHeight
    
    f = baseFillet
    
    t = cq.Workplane("XY").box(w + (f*2), d + (f*2), h)
    t = t.edges("|Z or >Z").fillet(f)

    inner = cq.Workplane("XY").box(w + (f*2)-3.2, d + (f*2)-3.2, h)
    inner = inner.edges("|Z or >Z").fillet(f - 1.6)
    inner = inner.translate([0,0,-1.6])
    
    
    r = ring(w + baseFillet,d + baseFillet,h, 1.2)
    r = r.translate([0, 0, -3.2])
    # show_object(r)
    
    
    ttw = w + baseFillet - 1.6 - (clearance*4)
    ttd = d + baseFillet - 1.6 - (clearance*4)
    tth = lip*2
    
    tt = cq.Workplane("XY").box(ttw, ttd, tth+0.1)
    tt = tt.edges("|Z").fillet(baseFillet/2)
    tt = tt.edges(">Z").fillet(1)
    tt = tt.translate([0,0,h/2-0.1])

    divot = cq.Workplane("YZ").box(
        depth - (baseFillet*2) + (clearance*2),
        height,
        10
        )
    
    divot = divot.translate([width/2 + 5 - 1.6, 0, 0])
    divot = divot.edges("|Z and <X").fillet(0.4)
    
    d2 = divot.mirror(mirrorPlane="YZ")
    divot = divot.union(d2)
    
    innerTrim = cq.Workplane("YZ").box(
        depth * 2,
        height,
        10
    )
    innerTrim = innerTrim.translate([width/2 + 5 - 1.6 - 1.6 - clearance, 0, 0])
    innerTrim2 = innerTrim.mirror(mirrorPlane="YZ")
    innerTrim = innerTrim.union(innerTrim2)
    
    if (width < depth):
        # add divots to >Y, <Y
        divot = cq.Workplane("XZ").box(
            width - (baseFillet*2) + (clearance*2),
            height,
            10
            )
        
        divot = divot.translate([0,depth/2 + 5 - 1.6 - clearance,0])
        divot = divot.edges("|Z and <Y").fillet(0.8)
        
        d2 = divot.mirror(mirrorPlane="XZ")
        divot = divot.union(d2)

        innerTrim = cq.Workplane("XZ").box(
            width * 2,
            height,
            10
        )
        innerTrim = innerTrim.translate([0, depth/2 + 5 - 1.6 - 1.6 - clearance, 0])
        innerTrim2 = innerTrim.mirror(mirrorPlane="XZ")
        innterTrim = innerTrim.union(innerTrim2)
            
    t = t.union(tt)
    
    inner = inner.cut(innerTrim)
    
    t = t.cut(inner)
    t = t.cut(divot)
    
    t = t.translate([0,0,h/2])
    
    return t

def sides():
    h = height - topHeight + lip
    rOffset = (h - (handleH*2) - (3.2))/2
    
    b = sidePanel(width, depth)
    b2 = sidePanel(depth, width).rotateAboutCenter([0,0,1], 90)

    sides = b.union(b2)
    
    r = ring(
        width + (sidePanelThick*2) + 1.6,
        depth + (sidePanelThick*2) + 1.6,
        1.6,
        sidePanelThick
    )
    r = r.edges(">Z or <Z").fillet(0.4)
    
    r = r.translate([0,0,0.8])
    
    r2 = r.translate([0,0,h/2 + rOffset])
    r = r.translate([0,0,h/2 - rOffset - 1.6])
    
    sides = sides.union(r2)
    sides = sides.union(r)
    return sides


bot = bottom()
show_object(bot)

topFinal = top()
# topFinal = topFinal.translate([0, 0, height - topHeight])
topFinal = topFinal.translate([width + 10, 0, 0])
show_object(topFinal)

# export the files as STLs
baseName = (str(math.floor(width)) + "x" + str(math.floor(depth)) + "x" + str(math.floor(height)) + ".stl")
cq.exporters.export(bot, "bottom_" + baseName)
cq.exporters.export(topFinal, "top_" + baseName)





