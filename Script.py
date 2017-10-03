import bpy
from bpy import context
from math import sin, cos, radians, pi

layerNumber = 7

# Init variables, size of object wanted
xSize = 0.5
ySize = 0.5
zSize = 0.5

# Select object, 0=plane, 1=cube, 2=circle, etc
selectObject = 0

#Circle Build Init angle variables, and the colour of the material
radialDistance = 1.0
noObjects = 8
revolutions = 1

helixIncrement = 1
radiusIncrement = 0.0

colourCustom = "White"
customRGB = [1.0, 1.0, 1.0]

# Common actions
rotateTransform = bpy.ops.transform.rotate #Rotate around Y up axis
resizeTransform = bpy.ops.transform.resize #Resiz according to the sizes above
cursor = context.scene.cursor_location # Get cursor location

#The Main, all shall bow to me
def Main():
    #Setting layer
    bpy.context.scene.layers[layerNumber] = True
    
    #Assigning primitives to a list and choosing by the order
    primsList = []
    primsList.append(bpy.ops.mesh.primitive_plane_add) #0
    primsList.append(bpy.ops.mesh.primitive_cube_add) #1
    primsList.append(bpy.ops.mesh.primitive_circle_add) #2
    primsList.append(bpy.ops.mesh.primitive_uv_sphere_add) #3
    primsList.append(bpy.ops.mesh.primitive_ico_sphere_add) #4
    primsList.append(bpy.ops.mesh.primitive_cylinder_add) #5
    primsList.append(bpy.ops.mesh.primitive_cone_add) #6
    primsList.append(bpy.ops.mesh.primitive_torus_add) #7
    
    myObject = primsList[selectObject]
    
    #Call functions
    InitColours()
    AddObjectsInCircle(myObject)

def InitColours():
    global colourRed 
    colourRed = bpy.data.materials.new("Red")
    colourRed.diffuse_color = (1,0,0)
    
    global colourGreen
    colourGreen = bpy.data.materials.new("Green")
    colourGreen.diffuse_color = (0,1,0)
    
    global colourBlue
    colourBlue = bpy.data.materials.new("Blue")
    colourBlue.diffuse_color = (0,0,1)   
    
    global colourCustom
    colourCustom = bpy.data.materials.new("Custom")
    colourCustom.diffuse_color = (customRGB)
    
def AddObjectsInCircle(myObject):
    #initial values
    tau = 2 * pi
    angle = tau / noObjects
    
    addObject = myObject      
    
    # Got to reset numbers first here
    theta = 0.0 #angle
    i = 0 #i is i no matte what language
    
    while theta < tau * revolutions:
        # Set coordinates for the new object
        x = cursor.x + (radialDistance + radiusIncrement * i) * cos(theta)
        y = cursor.y + (radialDistance + radiusIncrement * i) * sin(theta)
        z = cursor.z + helixIncrement * i
        
        # Add the object and then transform its size and rotation
        addObject(location = (x, y, z))
        resizeTransform(value = (xSize, ySize, zSize))
        rotateTransform(value = theta)  
        
        # Select zeroth object (i.e. most recent)
        activeObject = bpy.context.selected_objects[0]
        
        # Then change its colour
        activeObject.active_material = colourRed
        
        # Press Alt-A to activate the particle system
        activeObject.modifiers.new(name = "myParticle", type = "PARTICLE_SYSTEM")
        bpy.context.object.particle_systems[0].settings.lifetime = 150
        bpy.context.object.particle_systems[0].settings.frame_start = 25
        bpy.context.object.particle_systems[0].settings.frame_end = 150
        bpy.context.object.particle_systems[0].settings.lifetime_random = 5
                  
        # Increments 
        theta += angle
        i += 1
        
    #theta = 0.0 # reset theta
    
# Call the main function, otherwise it does nothing
Main()
