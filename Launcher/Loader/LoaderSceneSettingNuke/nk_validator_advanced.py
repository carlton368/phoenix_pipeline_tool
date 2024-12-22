try:
    from PySide6.QtWidgets import QMessageBox
except:
    from PySide2.QtWidgets import QMessageBox

import json
import os
import nuke
import re
import math

class NukeValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.successful_changes = []
        self.failed_changes = []
        self.user_home_path = os.path.expanduser('~')
        self.json_data = self.load_json_data()
        print('NukeValidator')

    def load_json_data(self):
        json_path = f"{self.user_home_path}/_phoenix_/Launcher/Loader/data_from_loader/json_from_loader.json"
        try:
            with open(json_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return {}

    def get_project_resolution(self):
        try:
            width = int(self.json_data.get('project_resolution_width', 0))
            height = int(self.json_data.get('project_resolution_height', 0))
            return width, height if width > 0 and height > 0 else (None, None)
        except ValueError:
            self.warnings.append("Invalid project resolution in JSON data")
            return None, None

    def check_project_settings(self):
        # Frame range check
        try:
            start = int(nuke.root()['first_frame'].value())
            end = int(nuke.root()['last_frame'].value())
            expected_start = int(self.json_data.get('start_frame', '0'))
            expected_end = int(self.json_data.get('end_frame', '0'))
            
            if start >= end:
                self.errors.append(f"Invalid frame range: {start}-{end}")
            elif expected_start > 0 and expected_end > 0:
                if start != expected_start or end != expected_end:
                    self.warnings.append(f"Frame range mismatch. Nuke: {start}-{end}, Expected: {expected_start}-{expected_end}")
            else:
                self.info.append(f"Current frame range: {start}-{end}. Unable to verify against expected range.")
        except ValueError:
            self.errors.append("Invalid frame range values")

        # Resolution check
        try:
            width = int(nuke.root().width())
            height = int(nuke.root().height())
            project_resolution_width, project_resolution_height = self.get_project_resolution()
            
            if project_resolution_width and project_resolution_height:
                if width == project_resolution_width and height == project_resolution_height:
                    self.info.append(f"Project resolution is correct: {width}x{height}")
                else:
                    self.warnings.append(f"Current resolution ({width}x{height}) does not match PROJECT's FINAL OUTPUT RESOLUTION ({project_resolution_width}x{project_resolution_height})")
            else:
                self.info.append(f"Current resolution: {width}x{height}. Unable to verify against project resolution.")
        except ValueError:
            self.errors.append("Invalid resolution values")

        # FPS check
        try:
            fps = float(nuke.root()['fps'].value())
            expected_fps = float(self.json_data.get('fps', 0))
            if expected_fps > 0:
                if math.isclose(fps, expected_fps, rel_tol=1e-9, abs_tol=0.0):
                    self.info.append(f"FPS is correct: {fps}")
                else:
                    self.warnings.append(f"FPS mismatch. Nuke: {fps}, Expected: {expected_fps}")
            else:
                self.info.append(f"Current FPS: {fps}. Unable to verify against expected FPS.")
        except ValueError:
            self.errors.append("Invalid FPS value")

    def check_render_settings(self):
        write_nodes = nuke.allNodes('Write') + nuke.allNodes('DeepWrite') + nuke.allNodes('WriteGeo') + nuke.allNodes('DeepWriteGeo')
        for node in write_nodes:
            self.validate_write_node(node)

    def validate_write_node(self, node):
        # 랜더될 파일 확장자 체크
        extension = node['file_type'].value()
        if extension not in ['exr']:
            self.warnings.append(f"{node.name()}의 확장자가 exr이 아닌 {extension}으로 랜더될 예정입니다.")

        # 컬러스페이스 체크
        if node.Class() == 'Write':
            color_space_knob = node.knob('colorspace')
            if color_space_knob:
                color_space = color_space_knob.value()
                if color_space not in ['ACES', 'ACEScg']:
                    self.warnings.append(f"{node.name()}의 컬러스페이스가 ACES 혹은 ACEScg가 아닌 {color_space}입니다.")
            else:
                self.errors.append(f"컬러스페이스 knob를 찾을 수 없습니다: {node.name()}")

        # output path 체크
        output_path = node['file'].value()
        if not output_path:
            self.errors.append(f"{node.name()}가 랜더될 파일 경로가 설정되지 않았습니다")
        elif not os.path.exists(os.path.dirname(output_path)):
            self.warnings.append(f"{node.name()}가 랜더될 파일 경로인 {os.path.dirname(output_path)}이 존재하지 않습니다")
        else:
            self.info.append(f"{node.name()}가 {os.path.dirname(output_path)}로 랜더될 예정입니다(경로 존재함)")

        # 랜더될 파일 이름이 네이밍 컨벤션에 맞는지 체크
        expected_prefix = self.json_data.get('sequence_name', '')
        if expected_prefix and not os.path.basename(output_path).startswith(expected_prefix):     
            self.warnings.append(f"{node.name()}가 랜더할 파일명이 시퀀스 네임으로 시작하지 않습니다. sequence_name: {expected_prefix}")

    def check_read_nodes(self):
        read_nodes = nuke.allNodes('Read')
        for node in read_nodes:
            self._check_read_node(node)

    def _check_read_node(self, node):
        # File existence check
        file_path = node['file'].value()
        if not file_path:
            self.warnings.append(f"No file path set for Read node {node.name()}")
        elif not os.path.exists(file_path):
            self.errors.append(f"File not found for Read node {node.name()}: {file_path}")

        # Frame range check
        try:
            node_start = int(node['first'].value())
            node_end = int(node['last'].value())
            if node_start > node_end:
                self.errors.append(f"Invalid frame range for Read node {node.name()}: {node_start}-{node_end}")
        except ValueError:
            self.errors.append(f"Invalid frame range values for Read node {node.name()}")

        # Color space check
        color_space = node['colorspace'].value()
        if color_space == 'default':
            self.warnings.append(f"Read node {node.name()} uses 'default' color space")

    def check_node_connections(self):
        for node in nuke.allNodes():
            if node.Class() not in ['Viewer', 'Write', 'DeepWrite', 'WriteGeo', 'DeepWriteGeo']:
                if not node.input(0) and not node.dependencies():
                    self.warnings.append(f"Node {node.name()} ({node.Class()}) is not connected to the node tree")

    def check_naming_conventions(self):
        for node in nuke.allNodes():
            if not re.match(r'^[a-zA-Z0-9_]+$', node.name()):
                self.warnings.append(f"Node {node.name()} does not follow naming convention (alphanumeric and underscore only)")

    def validate_nuke_script(self):
        print("Starting enhanced scene validation")
        self.errors = []
        self.warnings = []
        self.info = []

        self.check_project_settings()
        self.check_render_settings()
        self.check_read_nodes()
        self.check_node_connections()
        self.check_naming_conventions()

        return self.errors, self.warnings, self.info

    def setup_scene(self):
        print("Starting scene setup")
        try:
            self._set_frame_range()
            self._set_fps()
            self._set_project_format()
            print(f"Scene setup completed. Current frame range: {nuke.root()['first_frame'].value()}-{nuke.root()['last_frame'].value()}")
            return True, self.errors, self.warnings, self.successful_changes, self.failed_changes
        except Exception as e:
            print(f"Error during scene setup: {str(e)}")
            self.failed_changes.append("Scene setup")
            return False, self.errors, self.warnings, self.successful_changes, self.failed_changes
    def get_file_path(self):
        path=self.json_data.get('path', 'N/A')
        return path
    def initial_setup_scene(self):
        print("initial_Starting scene setup")
        try:
            self._set_frame_range()
            self._set_fps()
            self._set_project_format()
            # self._setup_write_node()
            print(f"Scene setup completed. Current frame range: {nuke.root()['first_frame'].value()}-{nuke.root()['last_frame'].value()}")
            return True, self.errors, self.warnings, self.successful_changes, self.failed_changes
        except Exception as e:
            print(f"Error during scene setup: {str(e)}")
            self.failed_changes.append("Scene setup")
            return False, self.errors, self.warnings, self.successful_changes, self.failed_changes
    def _set_frame_range(self):
        try:
            start_frame = int(self.json_data.get('start_frame', 0))
            end_frame = int(self.json_data.get('end_frame', 0))
            print(f"Attempting to set frame range: {start_frame}-{end_frame}")
            if start_frame > 0 and end_frame > 0 and start_frame <= end_frame:
                nuke.root()["first_frame"].setValue(start_frame)
                nuke.root()["last_frame"].setValue(end_frame)
                nuke.frame(start_frame)  # 시작 프레임으로 이동
                print(f"Frame range set to: {nuke.root()['first_frame'].value()}-{nuke.root()['last_frame'].value()}")
                self.successful_changes.append(f"Set frame range to {start_frame}-{end_frame}")
                for viewer in nuke.allNodes('Viewer'):
                    viewer['frame_range'].setValue(f"{start_frame}-{end_frame}")
            else:
                print(f"Invalid frame range: {start_frame}-{end_frame}")
                self.failed_changes.append(f"Set frame range - invalid data: {start_frame}-{end_frame}")
        except Exception as e:
            print(f"Error setting frame range: {str(e)}")
            self.failed_changes.append(f"Set frame range - error: {str(e)}")

    def _set_fps(self):
        try:
            fps = float(self.json_data.get('fps', 0))
            if fps > 0:
                current_fps = nuke.root()["fps"].value()
                nuke.root()["fps"].setValue(fps)
                if math.isclose(current_fps, fps, rel_tol=1e-9, abs_tol=0.0):
                    self.info.append(f"FPS was already correct: {fps}")
                else:
                    self.successful_changes.append(f"Set FPS from {current_fps} to {fps}")
            else:
                self.failed_changes.append("Failed to set FPS: invalid value")
        except ValueError:
            self.failed_changes.append("Failed to set FPS: invalid data type")

    def _setup_write_node(self):
        write_node = nuke.toNode("Write1") or nuke.createNode("Write")
        write_node.setName("Write1")
        exr_path = self._get_exr_path("Write1")
        if exr_path:
            write_node["file"].setValue(exr_path)
            write_node["file_type"].setValue("exr")
            write_node["colorspace"].setValue("ACES")
            self.successful_changes.append(f"Set up Write node with path: {exr_path}")
        else:
            self.failed_changes.append("Failed to set up Write node due to path issues")

    def _setup_deepwrite_node(self):
        deepwrite_node = nuke.toNode("DeepWrite1") or nuke.createNode("DeepWrite")
        deepwrite_node.setName("DeepWrite1")
        deep_exr_path = self._get_exr_path("DeepWrite1")
        if deep_exr_path:
            deepwrite_node["file"].setValue(deep_exr_path)
            deepwrite_node["file_type"].setValue("exr")
            self.successful_changes.append(f"Set up DeepWrite node with path: {deep_exr_path}")
        else:
            self.failed_changes.append("Failed to set up DeepWrite node due to path issues")

    def _set_project_format(self):
        width, height = self.get_project_resolution()
        if width and height:
            format_name = self.json_data.get('format_name', 'project_format')
            format_string = f"{width} {height} 0 0 {width} {height} 1 {format_name}"
            nuke.addFormat(format_string)
            nuke.root()["format"].setValue(format_name)
            self.successful_changes.append(f"Set project format to {width}x{height}")
        else:
            self.failed_changes.append("Failed to set project format: invalid resolution")

    def _get_exr_path(self, node_name):
        try:
            script_path = nuke.root().name()
            if not script_path:
                self.warnings.append("Unable to determine current Nuke script path.")
                return ""

            script_dir = os.path.dirname(script_path)
            script_name = os.path.basename(script_path)
            version_match = re.search(r'v(\d{3})', script_name)
            if not version_match:
                self.warnings.append("Unable to determine version from script name.")
                return ""

            version = version_match.group(0)
            version_folder = os.path.splitext(script_name)[0]
            exr_folder_path = os.path.join(script_dir, version_folder, "exr")
            os.makedirs(exr_folder_path, exist_ok=True)

            exr_file_name = f"{version_folder}_{node_name}.####.exr"
            exr_file_path = os.path.join(exr_folder_path, exr_file_name)

            return exr_file_path
        except Exception as e:
            self.warnings.append(f"Error generating EXR path: {str(e)}")
            return ""

    def get_script_validation_result(self):
        print("Getting script validation result")
        errors, warnings, info = self.validate_nuke_script()

        report = "Validation Results:\n\n"
        if errors:
            report += "Errors:\n" + "\n".join(f"- {error}" for error in errors) + "\n\n"
        if warnings:
            report += "Warnings:\n" + "\n".join(f"- {warning}" for warning in warnings) + "\n\n"
        if info:
            report += "Info:\n" + "\n".join(f"- {item}" for item in info) + "\n\n"

        if not (errors or warnings or info):
            report += "No issues found. The script passed all validation checks."

        print(f"Validation results:\n{report}")
    
        return report
    
    
    def get_scene_setting_result(self):
        print("Getting scene setting result")
        success, errors, warnings, successful_changes, failed_changes = self.setup_scene()

        report = "Scene Setting Results:\n\n"
        if successful_changes:
            report += "Successful Changes:\n" + "\n".join(f"- {change}" for change in successful_changes) + "\n\n"
        if failed_changes:
            report += "Failed Changes:\n" + "\n".join(f"- {change}" for change in failed_changes) + "\n\n"
        if errors:
            report += "Errors:\n" + "\n".join(f"- {error}" for error in errors) + "\n\n"
        if warnings:
            report += "Warnings:\n" + "\n".join(f"- {warning}" for warning in warnings) + "\n\n"

        if success and not (errors or warnings or failed_changes):
            report += "Scene setup completed successfully with no issues."

        print(f"Scene setting results:\n{report}")
        
        try:
            nuke.message(report)
        except:
            print("Unable to display message in Nuke. Printing report instead.")
            print(report)

        return success, errors, warnings, successful_changes, failed_changes