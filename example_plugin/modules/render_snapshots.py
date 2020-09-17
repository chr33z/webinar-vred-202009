import os
import subprocess
import vrVariantSets
import vrFileDialog
import vrFileIO
import vrRenderSettings
import vrCamera
from vrKernelService import *

def renderSnapshots(directory):
    '''
    Render all snapshots to the specified directory
    '''

    # Get all variant set groups and check if there is a group called "Snapshots"
    variantSetGroups = vrVariantSets.getGroupedVariantSets()
    if "Snapshots" in variantSetGroups:
        print("[VR][Workshop] Rendering snapshots to: " + directory)

        # Loop over all variant sets in the Snapshot group. The variable snapshot no contains the name of the variant set.
        for snapshot in variantSetGroups["Snapshots"]:
            # Conveniently our variant sets are called exactly like the corresponding viewpoint
            # Therefore we can jump the correct viewpoint using the same name as the variant set name
            vrCamera.jumpViewPoint(snapshot)

            # Create a file name
            filePath = os.path.join(directory, snapshot + ".png")
        
            # start rendering
            vrRenderSettings.setRenderFilename(filePath)
            vrRenderSettings.startRenderToFile(False)
    else:
        print("[VR][Workshop] There is no variant set group called 'Snapshots'.")

# Open a directory dialog and select a directory where to store the renderings
directory = vrFileDialog.getExistingDirectory("Select Snapshot Directory", vrFileIO.getFileIOFilePath())

def renderSnapshotsToDirectory(): 
    # If the user cancels the dialog or there is no such directory the variable 'directory' will be empty
    # In this case we tell the user and leave the script
    if directory:
        renderSnapshots(directory)
        subprocess.Popen(r'explorer /select,"' + directory + '"')
    else:
        print("[VR][Workshop] No valid directory selected.")
