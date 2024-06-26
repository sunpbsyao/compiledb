import os
import json
import util
import xml.etree.ElementTree as ET

ARM_COMPILER_CONFIG = [
    {
        "CC": "C:/Keil_v5/ARM/ARM/bin/armcc",
        "ASM": "C:/Keil_v5/ARM/ARM/bin/armasm",
        "DEFINE": "__ARMCC_VERSION=5060082",
        "ISYSTEM": "-isystem C:/Keil_v5/ARM/ARM/include",
        "RESOURCE": ""
    },
    {
        "CC": "C:/Keil_v5/ARM/ARMCLANG/bin/armclang",
        "ASM": "C:/Keil_v5/ARM/ARMCLANG/bin/armasm",
        "DEFINE": "__ARMCC_VERSION=6190000",
        "ISYSTEM": "-isystem C:/Keil_v5/ARM/ARMCLANG/include",
        "RESOURCE": "-resource-dir C:/Keil_v5/ARM/ARMCLANG/lib/clang/16.0.0"
    },
]

class Keil:
    def __init__(self, proj_file:str):
        self.proj_file = proj_file
        self.proj_path = os.path.abspath(os.path.dirname(self.proj_file))
        self.output_path = ""
        self.file_list = []
        self.c_define_list = []
        self.c_include_list = []
        self.asm_define_list = []
        self.asm_include_list = []
        self.compile_config = {}

    def __parse_ads(self, element: ET.Element, element_name: str):
        VariousControls = util.get_xml_element(
            util.get_xml_element(element, element_name), "VariousControls"
        )
        define_list = []
        if util.get_xml_element(VariousControls, "Define").text is not None:
            define_list = util.get_xml_element(VariousControls, "Define").text.split(",")
        include_list = []
        if util.get_xml_element(VariousControls, "IncludePath").text is not None:
            include_list = util.get_xml_element(VariousControls, "IncludePath").text.split(";")
        return define_list, include_list

    # 解析汇编文件和C文件的配置
    def __parse_armads(self, element: ET.Element):
        arm_ads = util.get_xml_element(element, "TargetArmAds")
        self.c_define_list, self.c_include_list = self.__parse_ads(arm_ads, "Cads")
        self.asm_define_list, self.asm_include_list = self.__parse_ads(arm_ads, "Aads")

    # 获取编译输出的目录
    def __parse_common_option(self, element: ET.Element):
        common_option = util.get_xml_element(element, "TargetCommonOption")
        output_path = util.get_xml_element(common_option, "OutputDirectory").text
        self.output_path = os.path.abspath(os.path.join(self.proj_path, output_path))

    # 获取工程使用的编译器版本，解析配置，
    def __parse_option(self, element: ET.Element):
        temp = util.get_xml_element(element, "uAC6").text
        self.compile_config = ARM_COMPILER_CONFIG[int(temp)]
        target_option = util.get_xml_element(element, "TargetOption")
        self.__parse_common_option(target_option)
        self.__parse_armads(target_option)

    # 获取到所有的文件
    def __parse_groups(self, element: ET.Element):
        group_elements = util.get_xml_element(element, "Groups").findall("Group")
        for group_element in group_elements:
            try:
                file_elements = util.get_xml_element(group_element, "Files").findall("File")
            except Exception as result:
                print(result)
                continue
            for file_element in file_elements:
                file_path = os.path.join(self.proj_path, util.get_xml_element(file_element, "FilePath").text)
                self.file_list.append(file_path)


    # 根据解析到的配置，拼接配置信息
    def __gen_config_str(self, include_list, define_list):
        define_str = f"-D{self.compile_config["DEFINE"]}"
        for define in define_list:
            define_str += f" -D{define.strip()}"
        include_str = ""
        for include in include_list:
            include_path = os.path.join(self.proj_path, include.strip())
            include_str += f" -I{include_path}"
        return f"{define_str} {include_str} {self.compile_config["ISYSTEM"]} {self.compile_config["RESOURCE"]}"


    # 在工程目录下生成compile_commands.json文件
    def __gen_compile_commands(self):
        # c file config
        c_config_str = self.__gen_config_str(self.c_include_list, self.c_define_list)
        # asm file config
        asm_config_str  = self.__gen_config_str(self.asm_include_list, self.asm_define_list)

        commands = []
        for file in self.file_list:
            command = {}
            obj_file = os.path.join(self.output_path, os.path.basename(file)).replace(".c", ".o")
            if util.is_asm_file(file):
                command["command"] = f"{self.compile_config["ASM"]} -c {file} -o {obj_file} {asm_config_str}"
            elif util.is_c_file(file):
                command["command"] = f"{self.compile_config["CC"]} -c {file} -o {obj_file} {c_config_str}" 
            else:
                continue
            command["directory"] = self.output_path
            command["file"] = file
            
            commands.append(command)
        
        with open(os.path.join(self.proj_path, "compile_commands.json"), "w") as f:
            json.dump(commands, f)
    

    def parse(self):
        tree = ET.parse(self.proj_file)
        root = tree.getroot()
        target = root.find("Targets").find("Target")
        try:
            self.__parse_option(target)
            self.__parse_groups(target)
        except Exception as result:
            print(result)

        self.__gen_compile_commands()


if __name__ == "__main__":
    Keil("./test/test.uvprojx").parse()
