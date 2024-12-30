""" Generar un archivo PUML con las dependencias de los módulos """

import ast
import os


def get_manifest_from_struct(path):
    """leer un manifest que esta dentro de una estructura de directorios
    revisar toda la estructura hasta encontrar un manifest.
    devolver el manifest y el path
    """
    ret = []
    for root, dirs, files in os.walk(path):
        set_files = {"__openerp__.py", "__manifest__.py"}.intersection(files)
        for file in list(set_files):
            manifest_file = f"{root}/{file}"
            manifest = load_manifest(manifest_file)
            name = root[2:]
            dependences = {name: manifest.get("depends", [])}
            ret.append(dependences)
    return ret


def load_manifest(filename):
    """Loads a manifest
    :param filename: absolute filename to manifest
    :return: manifest in dictionary format
    """
    manifest = ""
    with open(filename, encoding="utf-8") as _f:
        for line in _f:
            if line.strip() and line.strip()[0] != "#":
                manifest += line
        try:
            ret = ast.literal_eval(manifest)
        except Exception:
            return {"name": "none"}

        # incluir en el diagrama solo si el módulo es instalable
        if ret.get("installable", True):
            return ret

        return {"name": "none"}


def get_all_manifest(self, path):
    ret = []
    # busco en toda la estructura de directorios
    manifest, path = self.get_manifest_from_struct(path)
    if manifest:
        ret.append(load_manifest(manifest))

    # devuelvo el manifiesto o false si no esta
    return manifest


def get_all_manifest2(self, path):
    ret = []
    # busco en toda la estructura de directorios
    manifest, path = self.get_manifest_from_struct(path)
    if manifest:
        ret.append(load_manifest(manifest))
    # devuelvo el manifiesto o false si no esta
    return manifest


def write_puml():
    graph = get_manifest_from_struct("./")
    include = [list(x.keys())[0] for x in graph]
    with open("./dependencies.puml", "w", encoding="utf-8") as _f:
        _f.write('@startuml "Dependency Diagram"\n')
        for dep in graph:
            name = list(dep.keys())[0]
            depends = list(dep.values())[0]
            for module in depends:
                if name in include and module in include:
                    _f.write("%s -u-> %s\n" % (name, module))
        _f.write("@enduml\n")


write_puml()
