"""解析ini配置文件的模块"""
import configparser
import os


# 获取当前文件(__file__)的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在的目录
current_dir = os.path.dirname(current_file_path)


class ConfigParser:
    """解析ini配置文件的类"""
    DEFAULT_CONFIG_PATH = os.path.join(current_dir + '/../', 'config.ini')

    def __init__(self, path=None):  # Rename the 'config_path' parameter to 'path'
        self.config = configparser.ConfigParser()
        self.config_path = path or self.DEFAULT_CONFIG_PATH
        self._config_data = None

    def read_config(self):
        self.config.read(self.config_path, encoding='utf-8')
        self._config_data = {section: dict(self.config.items(
            section)) for section in self.config.sections()}
        return self._config_data

    def get_option(self, section, option):
        if self._config_data is not None:
            return self._config_data[section].get(option)
        else:
            raise ValueError(
                "Config data has not been loaded. Call read_config() first.")


# 以下部分允许直接从模块中加载配置
if __name__ == "__main__":
    import sys
    # 检查命令行参数数量，如果参数不足，使用默认的配置文件路径
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
    else:
        config_path = ConfigParser.DEFAULT_CONFIG_PATH

    section_option = input(
        "Enter section.option to get the value: ").split('.')
    parser = ConfigParser(config_path)
    config_data = parser.read_config()
    value = parser.get_option(section_option[0], section_option[1])
    print(f"The value of {section_option[0]}.{section_option[1]} is: {value}")

# 如果需要从命令行直接获取配置项的值，可以这样调用模块
# python config_parser.py path_to_your_config.ini general.option1
