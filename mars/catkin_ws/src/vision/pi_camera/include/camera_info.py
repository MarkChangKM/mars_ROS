
import os
import yaml

from sensor_msgs.msg import CameraInfo

# from cam_info_reader_node
def load_camera_info_2(filename):
    stream = file(filename, 'r')
    calib_data = yaml.load(stream)
    cam_info = CameraInfo()
    cam_info.width = calib_data['image_width']
    cam_info.height = calib_data['image_height']
    cam_info.K = calib_data['camera_matrix']['data']
    cam_info.D = calib_data['distortion_coefficients']['data']
    cam_info.R = calib_data['rectification_matrix']['data']
    cam_info.P = calib_data['projection_matrix']['data']
    cam_info.distortion_model = calib_data['distortion_model']
    return cam_info


# This one is used by the controllers...
def load_camera_info_3(robot):
    # Load camera information
    filename = (os.environ['DUCKIEFLEET_ROOT'] + "/calibrations/camera_intrinsic/" + robot + ".yaml")
    if not os.path.isfile(filename):
        dtu.logger.warn("no intrinsic calibration parameters for {}, trying default".format(robot))
        filename = (os.environ['DUCKIEFLEET_ROOT'] + "/calibrations/camera_intrinsic/default.yaml")
        if not os.path.isfile(filename):
            dtu.logger.error("can't find default either, something's wrong")
    calib_data = dtu.yaml_wrap.yaml_load_file(filename)
    cam_info = CameraInfo()
    cam_info.width = calib_data['image_width']
    cam_info.height = calib_data['image_height']
    cam_info.K = calib_data['camera_matrix']['data']
    cam_info.D = calib_data['distortion_coefficients']['data']
    cam_info.R = calib_data['rectification_matrix']['data']
    cam_info.P = calib_data['projection_matrix']['data']
    cam_info.distortion_model = calib_data['distortion_model']
    dtu.logger.info("Loaded camera calibration parameters for {} from {}".format(robot, os.path.basename(filename)))
    return cam_info
