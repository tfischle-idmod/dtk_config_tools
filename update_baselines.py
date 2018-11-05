#!/usr/bin/python

import sys
import xml.dom.minidom as xml
import json
import shutil
import os

def get_path_linux2windows(path):
    """try different paths linux vs. windows vs. windows on vm"""
    #linux
    if os.path.exists(path):
        return path

    # windows vm
    path_removed_mnt = os.path.join("//", path.split('/mnt/')[1:][0])
    if os.path.exists(path_removed_mnt):
        return path_removed_mnt

    # windows with z:
    path_z = os.path.join("Z:", path.split('/mnt/bayesianfil01/IDM')[1:][0])
    path_z = path_z.replace("/", "\\")
    if os.path.exists(path_z):
        return path_z

    print("path not found! : ", path)
    return None



if __name__ == '__main__':
    file_index = 1
    failedonly = False
    failedonlyLinux2Win = False
    allwindows = False
    bad_args = True

    if len(sys.argv) == 2:
        file_index = 1
        bad_args = False
    elif len(sys.argv) == 3 and sys.argv[1] == "-failedonly":
        file_index = 2
        failedonly = True
        bad_args = False
    elif len(sys.argv) == 3 and sys.argv[1] == "-failedonly-Linux2Win":
        file_index = 2
        bad_args = False
        failedonlyLinux2Win = True
    elif len(sys.argv) == 3 and sys.argv[1] == "-WinAll":
        file_index = 2
        bad_args = False
        allwindows = True
    
    if bad_args:
        print("usage: %s <-failedonly> xmlReportFile   To update files on a Windows machine with files of failing tests on a Windows machine (i.e. VS build) " % (sys.argv[0]) )
        print("usage: %s <-failedonly-Linux2Win> xmlReportFile    To update files on a Windows machine with files of failing tests on a Linux machine (i.e. Linux build)" % (sys.argv[0]))
        print("usage: %s <-allwindows> xmlReportFile    Copies all files from a Windwos machine to a windows machine (i.e. windows build)" % (
            sys.argv[0]))
    else:
        report_xml = xml.parse( sys.argv[ file_index ] )

        for node in report_xml.getElementsByTagName( 'failure' ):
            message = node.getAttribute( 'message' )
            (regression_name, icj_path) = message.split()[0], message.split()[9]

            if failedonly:
                reg_path = os.path.join( regression_name, 'output' )
                if os.path.exists( message.split()[9] ):
                    print( "copy "+message.split()[9]+" to " + reg_path )
                    shutil.copy( message.split()[9], reg_path )

            elif failedonlyLinux2Win:
                try:
                    reg_path = os.path.join(regression_name, 'output')
                    path_inset_chart = message.split()[9].replace("InsetChart.linux.json", "InsetChart.json")
                    path_inset_chart = get_path_linux2windows(path_inset_chart)
                    reg_path_linux = os.path.join(reg_path, "InsetChart.linux.json")
                    print( "copy " + path_inset_chart + " to " + reg_path_linux )
                    shutil.copy(path_inset_chart, reg_path_linux)
                except:
                    continue

            elif allwindows:
                try:
                    regression_name, icj_path = message.split()[0], message.split("found at")[1]    # there can spaces (" ") in filename
                    reg_path = os.path.join(regression_name, 'output')

                    # found no other way to create a valid path to a network share then to split and use join
                    dir_list = os.path.dirname(icj_path).split("\\")

                    path_network = ""
                    for item in dir_list[2:]:
                        path_network = os.path.join(path_network, item)

                    path_network = os.path.join("//", path_network)
                    path = os.path.join(path_network, os.path.basename(icj_path))
                    print("copy " + path + " to " + reg_path)
                    shutil.copy(path, reg_path)
                except:
                    print("ERROR copying ", path + " to " + reg_path)
                    continue
            else:
                source_dir = os.path.dirname(icj_path)
                print( 'Copying *.json and *.csv from {0} to {1}'.format( source_dir, regression_name ))
                for item in os.listdir(source_dir):
                    if item.split('.')[-1].lower() == 'json' or item.split('.')[-1].lower() == 'csv':
                        if os.name == "posix" and item != "InsetChart.json":
                            continue
                        source_file = os.path.join( source_dir, item )
                        if os.path.exists( source_file ):
                            dest_file = os.path.join( regression_name, 'output', item )
                            if os.name == "posix":
                                dest_file = dest_file.replace( "InsetChart.json", "InsetChart.linux.json" )
                            print( '\tCopying {0} to {1} ...'.format( source_file, dest_file ) )
                            shutil.copy( source_file, dest_file )
