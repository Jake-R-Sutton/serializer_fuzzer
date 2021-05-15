import os
import shutil
import time
import glob

class IPDLInterfaceDefinition:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.protocol_deps = [] # the protocols this protocol depends on
        self.ipdh_deps = [] # the header dependencies for this file
        self.cpp_header_deps = [] # the header dependencies for this file
        with open(path) as f:
            self.raw_text = f.readlines()
        self._process_deps()
        
    def _process_deps(self):
        for line in self.raw_text:
            l = line.strip()
            if l.startswith('include'):
                parsed = l.removeprefix('include').removesuffix(";").strip()
                if parsed.startswith('protocol'):
                    self.protocol_deps.append(parsed.removeprefix('protocol').strip())
                elif parsed.endswith(".h\""):
                    self.cpp_header_deps.append(parsed.removeprefix('\"').removesuffix('\"').strip())
                else:
                    self.ipdh_deps.append(parsed)

def refined_in(path, content):
    for line in content:
        if line.startswith(path):
            return line

def get_ipdl_file_paths():
    firefox_location = os.environ['IPDL_FF_LOCATION']
    path = os.path.join(firefox_location, "*/ipc/ipdl/ipdlsrcs.mk")
    ipd_sources_file_path = glob.glob(path, recursive=True)

    if len(ipd_sources_file_path) != 1:
        exit("something went wrong while hunting for ipdl sources")

    with open(ipd_sources_file_path[0]) as f:
        ipdlSrcsMk = f.readlines()

    all_srcs_pref = "ALL_IPDLSRCS := "
    just_files = line_after_prefix(ipdlSrcsMk, all_srcs_pref).removeprefix(all_srcs_pref)
    results = just_files.split(" ")

    # Observation: Some of the files are fully specified and others are not.
    for i, ipdl_path in enumerate(results):
        if refined_in(ipdl_path, ipdlSrcsMk):
           prefix = ipdl_path + ": "
           results[i] = line_after_prefix(ipdlSrcsMk, prefix).removeprefix(prefix) 

    return [p.strip() for p in results]

def line_after_prefix(content, prefix):
    for line in content:
        if prefix in line:
            return line

def drop_extension(filename):
    return os.path.splitext(filename)[0]

if __name__ == '__main__':
    ipdl_sources = get_ipdl_file_paths()
    print("Found {} sources from 'ipdlsrcs.mk'.".format(len(ipdl_sources)))
    for f in ipdl_sources:
        shutil.copy(f, 'ipdl/deps')