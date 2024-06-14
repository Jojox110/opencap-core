# Python libs
import os
import time
from typing import List, Dict, Union
import yaml
import shutil

# Other files in "Custom utils"/
from typeCheckers import can_be_int, can_be_float, is_valid_model


# Copied over parameters from downloadVideosFromServer that are not related to an OpenCap session or trial
def createFolderStructure(session_name: str, numberOfVideos: int = 2) -> None:
    """
    Creates the folder structure expected by OpenCap for videos.
    You do not need to call this function yourself. It will be called by addVideos()

    :param numberOfVideos: int
    :param session_name: str
    :return: None
    """
    # Check if the Data/ folder exists in the root directory of the project. If not, create it.
    data_dir = os.path.join("..\\Data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    """
    Naming system for "sessions" as OpenCap calls it: each folders name is the epoch time it was created at.
    The folder structure is the mostly as OpenCap for simplicity.
    Data/
        [epoch_time]
            MarkerData* (created by the augmentation code in main())
                PostAgumentation
                PreAgumentation
            Videos
                Cam{id}
                    InputMedia
                        {pose/category. Ex: neutral, calibration...}
                        ...
                   Other folders: TODO as im not sure what they're for atm or what creates them
        ...
        """

    if not os.path.exists(os.path.join(data_dir, session_name)):
        for i in range(numberOfVideos):
            if session_name:
                os.makedirs(os.path.join(data_dir, f"{session_name}", "Videos", f"Cam{i}", "InputMedia"),
                            exist_ok=True)
            else:
                os.makedirs(os.path.join(data_dir, f"{time.time()}", "Videos", f"Cam{i}", "InputMedia"),
                            exist_ok=True)


def readMetadataFromFile(input_filepath: str = "metadata.txt", output_filepath: str = "metadata.yaml") -> None:
    """
    :param input_filepath: path to the input file (string)
    :param output_filepath: path to the output file (string)
    :return: None. It will create a .yaml file containing the metadata of the input file.

    Reads metadata that would otherwise be obtained via OpenCap API.
    In order to read from a file, the following conditions must be met:\n
    - The file must be a .txt file
    - The content of the .txt file must be of the following format and only one per line:  [parameter] [space] [value]

    Example:
        height_m 1.62\n
        weight_kg 60

    The required parameters are:
        mass_kg float\n
        height_m float\n
        subject_name str\n
        device1 str\n
        device2 str\n
        device3 str (optional)\n
        device4 str (optional)

    A .yaml file will be created in the same directory as the .txt file to house the metadata.
    """
    metadata = {
        "checkerBoard": {}
    }

    # OpenCap followed Apple's naming scheme for product identifiers.
    # https://www.theiphonewiki.com/wiki/Models the names are under the "identifier" column
    required_user_parameters = {
        "mass_kg": False,
        "height_m": False,
        "subject_name": False,
        "device1": False,
        "device2": False,
        "device3": False,
        "device4": False,
    }
    required_user_parameters_types = {
        "mass_kg": "float",
        "height_m": "float",
        "subject_name": "str",
        "device1": "str",
        "device2": "str",
        "device3": "str",
        "device4": "str",
    }

    with open(input_filepath, "r") as f:
        for line_number, line in enumerate(f):
            line = line.strip()
            # if the format was followed correctly, [0] should be the parameter and [1] should be the value.
            content = line.split(" ")
            print(f"CONTENT: {content}")

            # Data validation
            if len(content) != 2:
                raise Exception(
                    f"Please recheck your formatting in {input_filepath} at line {line_number}. You should have two arguments: '[parameter] [value]'. You have {len(content)} arguments.")

            if content[0] not in required_user_parameters:
                raise Exception(
                    f"You have an invalid parameter at line {line_number}. The required parameters are: {required_user_parameters.keys()}")

            elif required_user_parameters_types[content[0]] == "float":
                if not can_be_float(content[1]):
                    raise Exception(
                        f"The value, {content[1]}, you passed alongside {content[0]} cannot be converted to a float as expected.")

            elif content[0] in ["device1", "device2", "device3", "device4"]:
                if not is_valid_model(content[1]):
                    raise Exception(f"The iOS device model, {content[1]}, is not a valid device identifier. "
                                    f"\nSee https://www.theiphonewiki.com/wiki/Models and look at the identifier column for that device.")

            metadata[content[0]] = content[1]
            required_user_parameters[content[0]] = True

    # Validate that all parameters have been filled
    for k, v in required_user_parameters.items():
        if not v and (k not in ["device3", "device4"]):
            print(f"v: {v} || k: {k}")
            raise Exception(f"You are missing one or more parameters."
                            f"\nThe required parameters are: {required_user_parameters.keys()}"
                            f"\nThe parameters you entered are: {metadata.keys()}")

    setInternalParameters(metadata)

    with open(output_filepath, "w") as f:
        yaml.dump(metadata, f)


def setInternalParameters(metadata: Dict[str, Union[str, Dict[str, Union[str, int]]]],
                          justCheckerParams: bool = False) -> None:
    """
    :param metadata: metadata dict (NOTE: it will be modified directly) (Dict[str, Union[str, Dict[str, Union[str, int]]]])
    :param justCheckerParams: set to True if you are doing a calibration task (bool)
    :return: nothing. The dict will be modified directly
    """
    # I know the metadata type hint is a mess, I copied over the same metadata dict structure that is used OpenCap.

    # For the moment being, the values assigned to the parameters are the values OpenCap assigns when not specified.
    if not justCheckerParams:
        metadata["posemodel"] = "openpose"
        metadata["openSimModel"] = "LaiUhlrich2022"
        metadata["filterFrequency"] = "default"
        metadata["augmentermodel"] = "v0.2"

    # Change as neccessary. The following data is for the recommended checkerboard on their get started page
    metadata["checkerBoard"]["squareSideLength_mm"] = 35
    metadata["checkerBoard"]["black2BlackCornersWidth_n"] = 5
    metadata["checkerBoard"]["black2BlackCornersHeight_n"] = 4
    metadata["checkerBoard"]["placement"] = "backWall"


def addVideos(session_name: str, pathVideo1: str, pathVideo2: str, pathVideo3: str = None,
              pathVideo4: str = None) -> None:
    """
    Add videos (must be .mov or .avi) to the Data/ directory of the given session.
    They will be copied from the path you provide

    :param session_name: name of the session (string)
    :param pathVideo1: path to video1 (string)
    :param pathVideo2: path to video2 (string)
    :param pathVideo3: path to video3 (optional, only if you have 3 cameras) (string)
    :param pathVideo4: path to video4 (optional, only if you have 4 cameras) (string)
    :return: None
    """
    path_to_videos = f"../Data/{session_name}/Videos"
    paths = [pathVideo1, pathVideo2]
    if pathVideo3:
        paths.append(pathVideo3)
    if pathVideo4:
        paths.append(pathVideo4)

    print("path to videos:")
    print(paths)

    createFolderStructure(session_name, len(paths))

    # When using "copy path" when right clicking on a file on Windows, it will wrap it around double quotes ("path") and use \ instead of /
    # This simply removes the double quotes if they exist and replaces any \ with \\ to avoid triggering an unwanted escape sequence
    for idx, path in enumerate(paths):
        if path[0] == path[-1] and path[0] == '\"':
            paths[idx] = path[1:-1]
        path.replace("\\", "\\\\")

    # Path validations
    for idx, path in enumerate(paths):
        if not os.path.exists(path):
            raise Exception(f"The path to video{idx} does not exist.")
        if path[-4:] not in [".mov", ".avi"]:
            raise Exception(f"Video{idx} and all other videos must be a .mov or a .avi file.")
        if idx in [3, 4] and not os.path.exists(f"{path_to_videos}/Cam{idx}/InputMedia"):
            raise Exception(f"You did not create a file structure that can handle {idx} videos."
                            f"\nPlease run createFileStructure and pass it the number of videos within [2, 4]."
                            f"\nIf you never put any other videos in {session_name}, "
                            f"you can safely delete the folder and use the name again if you wish.")

    for idx, path in enumerate(paths):
        video_location = os.path.join(path_to_videos, f"Cam{idx}/InputMedia")
        shutil.copy(path, video_location)


# testing
"""
paths = []
with open("test.txt", 'r') as f:
    for line in f:
        paths.append(line.strip())

addVideos("test", paths[0], paths[1])
"""