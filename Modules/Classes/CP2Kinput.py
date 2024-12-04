import json

from Classes.FileTypes.File import File


class CP2K:
    def __init__(self, data = None) -> None:
        self.data = data or {}

    def __setitem__(self, key, value) -> None:
        keys = key.split('.')
        d = self.data
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def __getitem__(self, key) -> dict:
        keys = key.split('.')
        d = self.data
        for k in keys:
            d = d[k]
        return d
    
    @classmethod
    def read(cls, jsonCP2Kfile: File) -> "CP2K":
        with open(jsonCP2Kfile, 'r') as f:
            data = json.load(f)
        return cls(data)

class FileCP2K:

    @staticmethod
    def write(cp2k_instance, file_path, file_format="json"):
        if file_format == "json":
            with open(file_path, 'w') as f:
                json.dump(cp2k_instance.data, f, indent=4)
        elif file_format == "inp":
            with open(file_path, 'w') as f:
                def write_recursive(d, indent=0):
                    try:
                        for k, v in d.items():
                            if isinstance(v, dict):
                                f.write(f"{' '*indent}&{k}\n")
                                write_recursive(v, indent+4)
                                f.write(f"{' '*indent}&END {k}\n")
                            elif isinstance(v, list):
                                strList = [str(i) for i in v]
                                f.write(f"{' '*indent}{k}\t")
                                f.write(f"\t".join(strList))
                                f.write(f"\n")
                            else:
                                f.write(f"{' '*indent}")
                                f.write(f"{k}\t{v}\n")
                    except AttributeError:
                        pass
                write_recursive(cp2k_instance.data)
    

cp2k = FileCP2K.read("cp2k_input.json")

cp2k["FORCE_EVAL.SUBSYS.CELL.ABC"] = [10.0, 15, 10]
cp2k["FORCE_EVAL.SUBSYS.COORD"] = {"N": [12.0, 15, 10]}

FileCP2K.write(cp2k, "cp2k_input_copy.inp", file_format="inp")
