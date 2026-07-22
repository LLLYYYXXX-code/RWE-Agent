"""
MIMIC-IV 代码→含义映射查询模块
===============================
支持离线查询: ICD诊断、ICD手术、实验室项目、ICU chartevents项目、HCPCS

用法:
    from mimic_dict import MimicDict
    d = MimicDict()
    
    # ICD 诊断
    d.icd_diag("I10")           # → "Essential (primary) hypertension"
    d.icd_diag("I10", ver=10)   # 同上,明确指定 ICD-10
    d.icd_diag("4019")          # → "Hypertension NOS" (ICD-9)
    
    # ICD 手术
    d.icd_proc("5A1221Z")       # → "Performance of Cardiac Output, Continuous"
    
    # 实验室项目
    d.labitem(50801)            # → "Alveolar-arterial Gradient"
    d.labitem("50801")          # 同上
    
    # ICU chartevents 项目
    d.icu_item(220045)          # → "Heart Rate"
    
    # 模糊搜索
    d.search_icd("hypertension")     # → [(code, title), ...]
    d.search_lab("creatinine")       # → [(itemid, label), ...]
    d.search_icu("heart rate")       # → [(itemid, label), ...]

数据来源: MIMIC-IV v3.1 (mimiciv_31)
"""

import json
import os
from typing import Optional, Union, List, Tuple, Dict

_JSON_PATH = os.path.join(os.path.dirname(__file__), "mimic_code_dict_lite.json")


class MimicDict:
    """MIMIC-IV 代码映射查询器"""
    
    def __init__(self, json_path: str = _JSON_PATH):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._dicts = data["dictionaries"]
        self._db = data.get("database", "?")
        self._generated = data.get("generated_at", "?")
        
        # 快捷引用
        self._icd10 = self._dicts.get("icd10_diagnoses", {}).get("entries", {})
        self._icd9 = self._dicts.get("icd9_diagnoses", {}).get("entries", {})
        self._labitems = self._dicts.get("labitems", {}).get("entries", {})
        self._icu_items = self._dicts.get("icu_items", {}).get("entries", {})
    
    def __repr__(self):
        return (f"MimicDict(db={self._db}, generated={self._generated}, "
                f"icd10={len(self._icd10)}, icd9={len(self._icd9)}, "
                f"labitems={len(self._labitems)}, icu_items={len(self._icu_items)})")
    
    # ---- ICD 诊断 ----
    def icd_diag(self, code: str, ver: Optional[int] = None) -> Optional[str]:
        """查询 ICD 诊断代码的含义。
        
        Args:
            code: ICD 代码,如 'I10', '4019' (自动处理空格/小数点)
            ver: ICD 版本 (9 或 10)。不指定时自动尝试两个版本。
        
        Returns:
            诊断全称,未找到返回 None
        """
        code = code.strip().replace(".", "")
        if ver == 10:
            return self._icd10.get(code)
        elif ver == 9:
            return self._icd9.get(code)
        else:
            return self._icd10.get(code) or self._icd9.get(code)
    
    # ---- ICD 手术 ----
    def icd_proc(self, code: str, ver: Optional[int] = None) -> Optional[str]:
        """查询 ICD 手术代码的含义 (需要完整版 dict)。
        
        精简版不含手术字典,请使用完整版 mimic_code_dict.json。
        """
        raise NotImplementedError(
            "精简版不含 ICD 手术字典。请使用完整版: "
            "MimicDict('/workspace/mimic_code_dict.json')"
        )
    
    # ---- 实验室项目 ----
    def labitem(self, itemid: Union[int, str]) -> Optional[str]:
        """查询实验室项目 itemid 对应的名称。
        
        Args:
            itemid: 实验室项目 ID,如 50801
        
        Returns:
            项目名称,未找到返回 None
        """
        return self._labitems.get(str(itemid))
    
    # ---- ICU chartevents 项目 ----
    def icu_item(self, itemid: Union[int, str]) -> Optional[str]:
        """查询 ICU chartevents itemid 对应的名称。
        
        Args:
            itemid: ICU 项目 ID,如 220045
        
        Returns:
            项目名称,未找到返回 None
        """
        return self._icu_items.get(str(itemid))
    
    # ---- 模糊搜索 ----
    def search_icd(self, keyword: str, limit: int = 20) -> List[Tuple[str, str, int]]:
        """模糊搜索 ICD 诊断代码。
        
        Args:
            keyword: 搜索关键词 (大小写不敏感)
            limit: 最大返回数
        
        Returns:
            [(code, title, icd_version), ...]
        """
        kw = keyword.lower()
        results = []
        for code, title in self._icd10.items():
            if title and kw in title.lower():
                results.append((code, title, 10))
                if len(results) >= limit:
                    return results
        for code, title in self._icd9.items():
            if title and kw in title.lower():
                results.append((code, title, 9))
                if len(results) >= limit:
                    return results
        return results[:limit]
    
    def search_lab(self, keyword: str, limit: int = 20) -> List[Tuple[str, str]]:
        """模糊搜索实验室项目。
        
        Returns:
            [(itemid, label), ...]
        """
        kw = keyword.lower()
        results = []
        for itemid, label in self._labitems.items():
            if label and kw in label.lower():
                results.append((itemid, label))
                if len(results) >= limit:
                    return results
        return results
    
    def search_icu(self, keyword: str, limit: int = 20) -> List[Tuple[str, str]]:
        """模糊搜索 ICU chartevents 项目。
        
        Returns:
            [(itemid, label), ...]
        """
        kw = keyword.lower()
        results = []
        for itemid, label in self._icu_items.items():
            if label and kw in label.lower():
                results.append((itemid, label))
                if len(results) >= limit:
                    return results
        return results
    
    # ---- 批量查询 ----
    def icd_diag_batch(self, codes: List[str]) -> Dict[str, Optional[str]]:
        """批量查询 ICD 诊断代码。"""
        return {c: self.icd_diag(c) for c in codes}
    
    def labitem_batch(self, itemids: List[Union[int, str]]) -> Dict[str, Optional[str]]:
        """批量查询实验室项目。"""
        return {str(i): self.labitem(i) for i in itemids}
    
    def icu_item_batch(self, itemids: List[Union[int, str]]) -> Dict[str, Optional[str]]:
        """批量查询 ICU 项目。"""
        return {str(i): self.icu_item(i) for i in itemids}


# ---- 便捷函数 ----
_default = None

def get_dict() -> MimicDict:
    """获取全局单例 MimicDict。"""
    global _default
    if _default is None:
        _default = MimicDict()
    return _default


def icd(code: str) -> Optional[str]:
    """快捷查询 ICD 诊断。"""
    return get_dict().icd_diag(code)


def lab(itemid: Union[int, str]) -> Optional[str]:
    """快捷查询实验室项目。"""
    return get_dict().labitem(itemid)


def icu(itemid: Union[int, str]) -> Optional[str]:
    """快捷查询 ICU 项目。"""
    return get_dict().icu_item(itemid)


# ---- 自测 ----
if __name__ == "__main__":
    d = MimicDict()
    print(d)
    print()
    
    # ICD
    print("ICD-10 I10  →", d.icd_diag("I10"))
    print("ICD-10 I50  →", d.icd_diag("I50"))
    print("ICD-9  4019 →", d.icd_diag("4019"))
    print("ICD-9  4280 →", d.icd_diag("4280"))
    print()
    
    # Lab
    print("Lab 50801 →", d.labitem(50801))
    print("Lab 50912 →", d.labitem(50912))
    print()
    
    # ICU
    print("ICU 220045 →", d.icu_item(220045))
    print("ICU 220050 →", d.icu_item(220050))
    print()
    
    # Search
    print("搜索 'sepsis':")
    for code, title, ver in d.search_icd("sepsis", limit=5):
        print(f"  ICD-{ver} {code}: {title}")
    
    print("\n搜索 'troponin' (lab):")
    for itemid, label in d.search_lab("troponin"):
        print(f"  {itemid}: {label}")
    
    print("\n搜索 'blood pressure' (ICU):")
    for itemid, label in d.search_icu("blood pressure"):
        print(f"  {itemid}: {label}")
