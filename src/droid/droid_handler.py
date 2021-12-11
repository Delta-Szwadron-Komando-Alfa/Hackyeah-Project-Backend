import subprocess
import os
import xml.etree.ElementTree as ET
import json

class FileIdentificator:
    def __init__(self, file_syg) -> None:
        self.file_syg = file_syg
        self.extenstionTag = "{http://www.nationalarchives.gov.uk/pronom/SignatureFile}Extension"
        self.formatTag = "{http://www.nationalarchives.gov.uk/pronom/SignatureFile}FileFormat"
        self.formatDatabase = ET.parse(self.file_syg)
        self.formatDict = self.init_file_ext_db()


    def init_file_ext_db(self) -> dict:
        format_dict = {}

        formats = [x for x in self.formatDatabase.getroot().iter() if x.tag == self.formatTag]
        for format in formats:
            desc = format.get("Name")
            puid = format.get("PUID")

            ext_list = []
            for child in format.iter():
                if child.tag == self.extenstionTag:
                    ext_list.append(child.text)

            format_dict[str(puid)] = (desc, ext_list)

        return format_dict
        

    def indentify_files(self, folder_name: str) -> str:

        full_path = os.getcwd() + "\\" + folder_name
        process_output = subprocess.run(["java", "-jar", "droid-command-line-6.5.jar", "-Nr", full_path, "-Ns", self.file_syg], capture_output=True)
        formated_output = process_output.stdout.decode("utf-8")

        files_with_ext = {}
        for line in formated_output.split("\r\n")[9:]:
            try:
                file_name, puid = line.split(",")
                desc, file_exts = self.formatDict.get(puid)
                files_with_ext[file_name.split("\\")[-1]] = (desc, file_exts)

            except ValueError:
                pass

            except TypeError:
                if puid == "Unknown":
                    files_with_ext[file_name.split("\\")[-1]] = (puid, [])

        return json.dumps(files_with_ext)


Client = FileIdentificator("DROID_SignatureFile_V99.xml")
print(Client.indentify_files("dla_uczestnikow"))