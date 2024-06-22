import os
import json
import util
import xml.etree.ElementTree as ET

ARM_COMPILER_CONFIG = {
    "CC": "C:/Program Files/IAR Systems/Embedded Workbench 9.0/arm/bin/iccarm",
    "ASM": "C:/Program Files/IAR Systems/Embedded Workbench 9.0/arm/bin/iasmarm",
    "DEFINE": "-D__ICCARM__=1 -D__IAR_SYSTEMS_ICC__=9",
    # "ISYSTEM": "-isystem 'C:/Program Files/IAR Systems/Embedded Workbench 9.0/arm/inc/c'",
    # 空格路径有点问题
    "ISYSTEM": ""
}

class Iar:
    def __init__(self, proj_file:str):
        self.proj_file = proj_file
        self.proj_path = os.path.abspath(os.path.dirname(self.proj_file))
        self.output_path = ""
        self.file_list = []
        self.c_define_list = []
        self.c_include_list = []
        self.asm_define_list = []
        self.asm_include_list = []
        self.compile_config = ARM_COMPILER_CONFIG

    def __find_xml_element(self, elements, name):
        for element in elements:
            if util.get_xml_element(element, "name").text == name:
                return element
        raise Exception(f"contain {name} element not found")


    # 解析配置
    def __parse_configuration(self, element: ET.Element):
        configurations = element.findall("configuration")
        if len(configurations) == 0:
            raise Exception("not found configuration")
        # TODO：暂时支持第一个configuration （一般为Debug）
        settings = configurations[0].findall("settings")
        try:
            # 获取三个配置节点
            general = self.__find_xml_element(settings, "General")
            iccarm = self.__find_xml_element(settings, "ICCARM")
            aarm = self.__find_xml_element(settings, "AARM")

            # 获取编译输出文件夹
            options = util.get_xml_element(general, "data").findall("option")
            obj_path = self.__find_xml_element(options, "ObjPath")
            self.output_path = os.path.abspath(os.path.join(self.proj_path, util.get_xml_element(obj_path, "state").text))
            
            # 获取c文件的宏定义和头文件列表
            options = util.get_xml_element(iccarm, "data").findall("option")
            define = self.__find_xml_element(options, "CCDefines")
            include = self.__find_xml_element(options, "CCIncludePath2")
            define_states = define.findall("state")
            for define_state in define_states:
                self.c_define_list.append(define_state.text)

            include_states = include.findall("state")
            for include_state in include_states:
                path = include_state.text.strip().replace("$PROJ_DIR$", self.proj_path)
                path = os.path.abspath(path)
                self.c_include_list.append(path)

            # 获取汇编文件的宏定义和头文件列表
            options = util.get_xml_element(aarm, "data").findall("option")
            define = self.__find_xml_element(options, "ADefines")
            include = self.__find_xml_element(options, "AUserIncludes")
            define_states = define.findall("state")
            for define_state in define_states:
                self.asm_define_list.append(define_state.text)

            include_states = include.findall("state")
            for include_state in include_states:
                path = include_state.text.strip().replace("$PROJ_DIR$", self.proj_path)
                path = os.path.abspath(path)
                self.asm_include_list.append(path)
            
        except Exception as result:
            print(result)
            return
            
    # 解析文件
    def __parse_group(self, element: ET.Element):
        for temp in element.iter():
            if temp.tag == "file":
                file = util.get_xml_element(temp, "name").text.strip().replace("$PROJ_DIR$", self.proj_path)
                self.file_list.append(os.path.abspath(file))


    # 根据解析到的配置，拼接配置信息
    def __gen_config_str(self, include_list, define_list):
        define_str = self.compile_config["DEFINE"]
        for define in define_list:
            if define != None:
                define_str += f" -D{define.strip()}"
        include_str = ""
        for include in include_list:
            if include != None:
                include_path = os.path.join(self.proj_path, include.strip())
                include_str += f" -I{include_path}"
        return f"{define_str} {include_str} {self.compile_config["ISYSTEM"]}"


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
        try:
            self.__parse_configuration(root)
            self.__parse_group(root)
        except Exception as result:
            print(result)
            return

        self.__gen_compile_commands()

if __name__ == "__main__":
    Iar("./test/test.ewp").parse()
