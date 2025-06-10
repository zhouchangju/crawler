#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大学英文名转中文名翻译脚本
支持多种翻译方案：百度翻译API、Google翻译、有道翻译等
"""

import json
import requests
import hashlib
import random
import time
from pathlib import Path


class UniversityNameTranslator:
    """大学名称翻译器"""
    
    def __init__(self):
        # 预定义的大学名称映射（常见大学的标准中文翻译）
        self.university_mapping = {
            # 美国大学
            "Massachusetts Institute of Technology (MIT)": "麻省理工学院",
            "Stanford University": "斯坦福大学",
            "Harvard University": "哈佛大学",
            "California Institute of Technology (Caltech)": "加州理工学院",
            "University of Chicago": "芝加哥大学",
            "University of Pennsylvania": "宾夕法尼亚大学",
            "Yale University": "耶鲁大学",
            "Columbia University": "哥伦比亚大学",
            "Princeton University": "普林斯顿大学",
            "Cornell University": "康奈尔大学",
            
            # 英国大学
            "University of Oxford": "牛津大学",
            "University of Cambridge": "剑桥大学",
            "Imperial College London": "帝国理工学院",
            "UCL (University College London)": "伦敦大学学院",
            "London School of Economics and Political Science (LSE)": "伦敦政治经济学院",
            "King's College London": "伦敦国王学院",
            "University of Edinburgh": "爱丁堡大学",
            "University of Manchester": "曼彻斯特大学",
            "University of Warwick": "华威大学",
            
            # 中国大学
            "Tsinghua University": "清华大学",
            "Peking University": "北京大学",
            "Fudan University": "复旦大学",
            "Zhejiang University": "浙江大学",
            "Shanghai Jiao Tong University": "上海交通大学",
            "University of Science and Technology of China": "中国科学技术大学",
            "Nanjing University": "南京大学",
            "Sun Yat-sen University": "中山大学",
            "Tongji University": "同济大学",
            "Wuhan University": "武汉大学",
            "Harbin Institute of Technology": "哈尔滨工业大学",
            "Beijing Normal University": "北京师范大学",
            "Xi'an Jiaotong University": "西安交通大学",
            "Xi'an Jiaotong Liverpool University": "西交利物浦大学",
            # 处理Unicode单引号版本
            "Xi'an Jiaotong University": "西安交通大学",
            "Xi'an Jiaotong Liverpool University": "西交利物浦大学",
            "Huazhong University of Science and Technology": "华中科技大学",
            "Tianjin University": "天津大学",
            "Nankai University": "南开大学",
            "Beijing Institute of Technology": "北京理工大学",
            "Beihang University (former BUAA)": "北京航空航天大学",
            "Shandong University": "山东大学",
            "South China University of Technology": "华南理工大学",
            "Xiamen University": "厦门大学",
            "University of Science and Technology Beijing": "北京科技大学",
            "Shanghai University": "上海大学",
            "Sichuan University": "四川大学",
            "Southeast University": "东南大学",
            "Jilin University": "吉林大学",
            "Central South University": "中南大学",
            "China University of Geosciences": "中国地质大学",
            "East China Normal University": "华东师范大学",
            "Northwestern Polytechnical University": "西北工业大学",
            "Dalian University of Technology": "大连理工大学",
            "East China University of Science and Technology": "华东理工大学",
            "Hunan University": "湖南大学",
            "University of Electronic Science and Technology of China": "电子科技大学",
            "China Agricultural University": "中国农业大学",
            "Nanjing University of Science and Technology": "南京理工大学",
            "Renmin (People's) University of China": "中国人民大学",
            "Shenzhen University": "深圳大学",
            "Soochow University": "苏州大学",
            "Chongqing University": "重庆大学",
            "Beijing University of Technology": "北京工业大学",
            "Jinan University (China)": "暨南大学",
            "Lanzhou University": "兰州大学",
            "Northwest University (China)": "西北大学",
            "Beijing Foreign Studies University": "北京外国语大学",
            "Beijing Jiaotong University": "北京交通大学",
            "Beijing University of Chinese Medicine": "北京中医药大学",
            "Beijing University of Posts and Telecommunications": "北京邮电大学",
            "Harbin Engineering University": "哈尔滨工程大学",
            "Nanjing University of Aeronautics and Astronautics": "南京航空航天大学",
            "Wuhan University of Technology": "武汉理工大学",
            "China University of Political Science and Law": "中国政法大学",
            "Shanghai International Studies University": "上海外国语大学",
            "University of International Business and Economics": "对外经济贸易大学",
            "Shanghai University of Finance and Economics": "上海财经大学",
            "Southwest University": "西南大学",
            "Southern University of Science and Technology (SUSTech)": "南方科技大学",
            # 手动补充
            "Asia University Taiwan": "台湾亚洲大学",
            "Beijing University of Chemical Technology": "北京化工大学",
            "Chaoyang University of Technology": "台湾朝阳科技大学",
            "China University of Mining and Technology": "中国矿业大学",
            "China University of Petroleum, Beijing": "中国石油大学（北京）",
            "Donghua University": "东华大学",
            "Hohai University": "河海大学",
            "Huazhong Agricultural University": "华中农业大学",
            "Jiangnan University": "江南大学",
            "Kaohsiung Medical University": "台湾高雄医学大学",
            "Nanjing Agricultural University": "南京农业大学",
            "Nanjing Normal University": "南京师范大学",
            "National Chiao Tung University": "台湾国立交通大学",
            "National Yang Ming University": "台湾国立阳明大学",
            "Northwest Agriculture and Forestry University": "西北农林科技大学",
            "Ocean University of China": "中国海洋大学",
            "Shanghai Normal University": "上海师范大学",
            "Zhengzhou University": "郑州大学",

            
            # 香港大学
            "The University of Hong Kong": "香港大学",
            "The Hong Kong University of Science and Technology": "香港科技大学",
            "The Chinese University of Hong Kong (CUHK)": "香港中文大学",
            "City University of Hong Kong (CityUHK)": "香港城市大学",
            "The Hong Kong Polytechnic University": "香港理工大学",
            "Hong Kong Baptist University": "香港浸会大学",
            "Lingnan University, Hong Kong": "香港岭南大学",
            
            # 台湾大学
            "National Taiwan University (NTU)": "国立台湾大学",
            "National Tsing Hua University - NTHU": "国立清华大学",
            "National Cheng Kung University (NCKU)": "国立成功大学",
            "National Yang Ming Chiao Tung University (NYCU)": "国立阳明交通大学",
            "National Taiwan University of Science and Technology (Taiwan Tech)": "国立台湾科技大学",
            "National Taiwan Normal University (NTNU)": "国立台湾师范大学",
            "Taipei Medical University (TMU)": "台北医学大学",
            "National Sun Yat-sen University": "国立中山大学",
            "National Taipei University of Technology": "国立台北科技大学",
            "Chang Gung University": "长庚大学",
            "National Central University": "国立中央大学",
            "National Chengchi University": "国立政治大学",
            "National Chung Hsing University": "国立中兴大学",
            "National Chung Cheng University": "国立中正大学",
            "Chang Jung Christian University": "长荣大学",
            "Chung Yuan Christian University": "中原大学",
            "Feng Chia University": "逢甲大学",
            "Fu Jen Catholic University": "辅仁大学",
            "National Dong Hwa University": "国立东华大学",
            "National Taiwan Ocean University": "国立台湾海洋大学",
            "Yuan Ze University": "元智大学",
            "National Taipei University": "国立台北大学",
            "Soochow University (Taiwan)": "东吴大学",
            "Tamkang University": "淡江大学",
            "Tunghai University": "东海大学",
            
            # 澳门大学
            "University of Macau": "澳门大学",
            "Macau University of Science and Technology": "澳门科技大学",
            
            # 其他知名大学
            "University of Tokyo": "东京大学",
            "Kyoto University": "京都大学",
            "Seoul National University": "首尔国立大学",
            "National University of Singapore (NUS)": "新加坡国立大学",
            "Nanyang Technological University, Singapore (NTU)": "南洋理工大学",
            "University of Melbourne": "墨尔本大学",
            "Australian National University (ANU)": "澳大利亚国立大学",
            "University of Sydney": "悉尼大学",
            "University of Toronto": "多伦多大学",
            "McGill University": "麦吉尔大学",
        }
    
    def normalize_university_name(self, name):
        """
        标准化大学名称，处理不同类型的引号和空格
        
        Args:
            name (str): 原始大学名称
            
        Returns:
            str: 标准化后的名称
        """
        # 将Unicode单引号转换为ASCII单引号
        normalized = name.replace('\u2019', "'").replace('\u2018', "'")
        # 去除多余的空格
        normalized = ' '.join(normalized.split())
        return normalized
    
    def get_predefined_translation(self, english_name):
        """
        从预定义映射表中获取翻译
        
        Args:
            english_name (str): 英文校名
            
        Returns:
            str or None: 中文校名，如果不存在则返回None
        """
        # 标准化输入名称
        normalized_input = self.normalize_university_name(english_name)
        
        # 直接匹配（标准化后）
        for eng_name, chi_name in self.university_mapping.items():
            normalized_mapping = self.normalize_university_name(eng_name)
            if normalized_input == normalized_mapping:
                return chi_name
        
        # 模糊匹配（去除括号内容和尾部空格）
        clean_name = normalized_input.split('(')[0].strip()
        for eng_name, chi_name in self.university_mapping.items():
            normalized_mapping = self.normalize_university_name(eng_name)
            clean_eng_name = normalized_mapping.split('(')[0].strip()
            if clean_name == clean_eng_name or clean_name in normalized_mapping or normalized_mapping.startswith(clean_name):
                return chi_name
        
        return None
    
    def translate_with_baidu(self, text, app_id=None, secret_key=None):
        """
        使用百度翻译API进行翻译
        
        Args:
            text (str): 要翻译的文本
            app_id (str): 百度翻译API的APP ID
            secret_key (str): 百度翻译API的密钥
            
        Returns:
            str or None: 翻译结果
        """
        if not app_id or not secret_key:
            print("需要提供百度翻译API的APP ID和密钥")
            return None
        
        url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        from_lang = 'en'
        to_lang = 'zh'
        salt = random.randint(32768, 65536)
        
        # 构建签名
        sign_str = app_id + text + str(salt) + secret_key
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
        params = {
            'q': text,
            'from': from_lang,
            'to': to_lang,
            'appid': app_id,
            'salt': salt,
            'sign': sign
        }
        
        try:
            response = requests.get(url, params=params)
            result = response.json()
            
            if 'trans_result' in result:
                return result['trans_result'][0]['dst']
            else:
                print(f"百度翻译API错误: {result}")
                return None
        except Exception as e:
            print(f"百度翻译API调用失败: {e}")
            return None
    
    def translate_with_youdao(self, text):
        """
        使用有道翻译（免费接口）进行翻译
        
        Args:
            text (str): 要翻译的文本
            
        Returns:
            str or None: 翻译结果
        """
        url = 'http://fanyi.youdao.com/translate'
        data = {
            'type': 'AUTO',
            'i': text,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'ue': 'UTF-8',
            'action': 'FY_BY_CLICKBUTTON',
            'typoResult': 'true'
        }
        
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if 'translateResult' in result and result['translateResult']:
                return result['translateResult'][0][0]['tgt']
            else:
                print(f"有道翻译错误: {result}")
                return None
        except Exception as e:
            print(f"有道翻译调用失败: {e}")
            return None
    
    def translate_with_googletrans(self, text):
        """
        使用googletrans库进行翻译
        
        Args:
            text (str): 要翻译的文本
            
        Returns:
            str or None: 翻译结果
        """
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, src='en', dest='zh')
            return result.text
        except ImportError:
            print("需要安装googletrans库: pip install googletrans==4.0.0-rc1")
            return None
        except Exception as e:
            print(f"Google翻译调用失败: {e}")
            return None
    
    def translate_university_name(self, english_name, method='predefined', **kwargs):
        """
        翻译大学名称
        
        Args:
            english_name (str): 英文校名
            method (str): 翻译方法 ('predefined', 'baidu', 'youdao', 'google')
            **kwargs: 其他参数（如百度翻译的API密钥）
            
        Returns:
            str: 中文校名
        """
        if method == 'predefined':
            result = self.get_predefined_translation(english_name)
            if result:
                return result
            else:
                # 如果预定义中没有，则尝试其他方法
                print(f"预定义映射中未找到 '{english_name}'，尝试在线翻译...")
                return self.translate_university_name(english_name, method='youdao')
        
        elif method == 'baidu':
            return self.translate_with_baidu(english_name, **kwargs)
        
        elif method == 'youdao':
            return self.translate_with_youdao(english_name)
        
        elif method == 'google':
            return self.translate_with_googletrans(english_name)
        
        else:
            print(f"不支持的翻译方法: {method}")
            return english_name
    
    def translate_university_data(self, input_file, output_file, method='predefined', **kwargs):
        """
        批量翻译大学数据文件中的大学名称
        
        Args:
            input_file (str): 输入文件路径
            output_file (str): 输出文件路径
            method (str): 翻译方法
            **kwargs: 其他参数
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                universities = json.load(f)
            
            print(f"开始翻译 {len(universities)} 所大学的名称...")
            
            for i, university in enumerate(universities):
                english_name = university.get('title', '')
                if english_name:
                    # 翻译大学名称
                    chinese_name = self.translate_university_name(english_name, method, **kwargs)
                    university['title_zh'] = chinese_name
                    
                    print(f"{i+1:3d}. {english_name} -> {chinese_name}")
                    
                    # 添加延时，避免API限制
                    if method in ['youdao', 'baidu'] and i % 10 == 9:
                        time.sleep(1)
            
            # 保存结果
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(universities, f, ensure_ascii=False, indent=2)
            
            print(f"翻译完成！结果已保存到 {output_file}")
            
        except Exception as e:
            print(f"批量翻译失败: {e}")


def process_all_parsed_files():
    """
    处理 data/parsed 目录下的所有文件，添加中文翻译
    """
    translator = UniversityNameTranslator()
    script_dir = Path(__file__).parent
    parsed_dir = script_dir / "data" / "parsed"
    
    if not parsed_dir.exists():
        print(f"解析数据目录 {parsed_dir} 不存在")
        return
    
    # 查找所有JSON文件（排除已有中文翻译的文件）
    json_files = [f for f in parsed_dir.glob("*.json") if not f.name.endswith("_with_chinese.json")]
    
    if not json_files:
        print("未找到需要翻译的JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个文件需要翻译")
    
    for input_file in sorted(json_files):
        year = input_file.stem  # 获取文件名（不含扩展名）
        output_file = parsed_dir / f"{year}_with_chinese.json"
        
        print(f"\n处理文件: {input_file.name}")
        
        try:
            translator.translate_university_data(input_file, output_file, method='predefined')
            print(f"✅ 成功翻译并保存到: {output_file.name}")
        except Exception as e:
            print(f"❌ 处理文件 {input_file.name} 时出错: {e}")
    
    print(f"\n🎉 批量翻译完成！共处理了 {len(json_files)} 个文件")


def main():
    """主函数"""
    translator = UniversityNameTranslator()
    
    # 示例用法1：单个大学名称翻译
    print("=== 单个大学名称翻译示例 ===")
    test_names = [
        "Massachusetts Institute of Technology (MIT)",
        "University of Oxford",
        "Tsinghua University",
        "Stanford University",
        "Some Unknown University"
    ]
    
    for name in test_names:
        chinese_name = translator.translate_university_name(name)
        print(f"{name} -> {chinese_name}")
    
    print("\n=== 批量翻译所有文件 ===")
    # 批量处理所有解析后的文件
    process_all_parsed_files()


if __name__ == "__main__":
    main() 