import os
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        base_path: str = Field(
            default="~/castle/",
            description="the folder where AI is allowed to write files ",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.path = os.path.expanduser(self.valves.base_path)

    def reader(self, filename):
        """
        used for reading file
            param => filename : the file's name that we want to read
            returns => list of contents of the file, error string
        """
        try:
            verified_path = self.safe_path(filename)
            read_variable = open(verified_path, "r")
            read_list = []

            for line in read_variable:
                read_list.append(line.strip())

            read_variable.close()
            return read_list

        except Exception as e:
            return f"Error in reading the file {e}"

    def appender(self, filename, content):
        """
        used for appending content to file that already exists

        param => filename : relative path and name of the file
                 content : content that you want to write in the file

        returns => error string , success string
        """

        try:
            verified_path = self.safe_path(filename)
            write_variable = open(verified_path, "a")
            write_variable.write(content)
            write_variable.close()
            return "done"

        except Exception as e:
            return f"error occurred in writing file {e}"

    def writer(self, filename, content):
        """
        used for writing content from scratch to file that already exists

        param => filename : relative path and name of the file
                 content : content that you want to write in the file

        returns => error string , success string
        """

        try:
            verified_path = self.safe_path(filename)
            with open(verified_path, "w") as write_variable:
                write_variable.write(content)
            return "done"
        except Exception as e:
            return f"error occurred in writing file {e}"

    def creater(self, filename):
        """
        used to create empty file

        param => filename: relative path and name of the file

        returns => either returns success string or error string
        """
        try:
            verified_path = self.safe_path(filename)
            with open(verified_path, "x") as create_variable:
                return "done"

        except Exception:
            return f"there was an error in opening and creating the file {filename}"

    def directory_creater(self, dir_name):
        """
        used to create a directory

        param => dir_name: relative path and name of the directory

        returns => either returns success string or error string
        """
        try:
            verified_path = self.safe_path(dir_name)
            os.mkdir(verified_path)
            return "done"

        except Exception as e:
            return f"there was an error in creating directory {e}"

    def remover(self, filename):
        """
        used to delete or remove a file

        param => filename: relative path and name of the file

        returns => either returns success string or error string

        """
        try:
            verified_path = self.safe_path(filename)
            os.remove(verified_path)
            return "done"

        except Exception as e:
            return f"the file was not found {e}"

    def directory_remover(self, dir_name):
        """
        used to remove a directory that is empty

        param => dir_name: relative path and name of the directory

        returns => either returns success string or error string

        """
        try:
            verified_path = self.safe_path(dir_name)
            os.rmdir(verified_path)
            return "done"

        except Exception as e:
            return f"there was an error in deleting the directory {e}"

    def list_directory(self, dir_name="."):
        """
        used to list the contents of a directory

        param => dir_name : relative path and name of the directory

        returns => a dictionary with keys "dir" and "file" that each has a value
                   which is a list of directories/files that are inside the directory in question
                   and a key name "dir_path" which has the relative path and name of the said directory
                   or returns an error string
        """
        try:
            verified_path = self.safe_path(dir_name)
            tmp_path = verified_path
            mixed_list = os.listdir(tmp_path)

            sorted_dict = {"dir": [], "file": [], "dir_path": tmp_path}

            for listing in mixed_list:
                if os.path.isdir(os.path.join(tmp_path, listing)):
                    sorted_dict["dir"].append(listing)
                else:
                    sorted_dict["file"].append(listing)

            return sorted_dict

        except Exception as e:
            return f"an unexpected exception occurred while reading contents of the directory {e}"

    def search(self, filename):
        """
        used for searching files throughout a directory

        params => filename : the name of the file you want to search

        returns => the relative_path of the file if found or error string or not found string
        """
        try:
            to_check = ["."]
            while to_check:
                current_directory = to_check.pop()
                content_dict = self.list_directory(current_directory)

                if not isinstance(content_dict, dict):
                    continue

                if filename in content_dict["file"]:
                    return os.path.join(content_dict["dir_path"], filename)

                for each_entry in content_dict["dir"]:
                    to_check.append(os.path.join(content_dict["dir_path"], each_entry))

            return "the file was not found"

        except Exception as e:
            return f"there was a problem while searching {e}"

    def safe_path(self, relative_path):
        """
        used to check if the relative path is trying to walk back to main system and stop it

        param => relative_path : the path that we want to check

        returns => verified path or error string

        """
        target_path = os.path.abspath(os.path.join(self.path, relative_path))
        basepath = os.path.abspath(self.path)

        if os.path.commonpath([target_path, basepath]) != basepath:
            raise ValueError("attempt to escape home directory")

        return target_path


if __name__ == "__main__":
    pass
    tools = Tools()
    tools.writer("pao/textings", "does,it work?")
    tools.list_directory("pao")
    print(tools.search("textings"))
