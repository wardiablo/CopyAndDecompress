import os
import glob
import shutil
import sys
import subprocess
from shutil import copytree, ignore_patterns, copy2
from fnmatch import fnmatch, filter
from os.path import isdir, join

#Copy and ignore files in src
#For example, copytree(ets_report_src_dir, ets_report_dst_dir, ignore=ignore_patterns('*Top*', '*Per*', '*.zip', '.DS_Store', 'hour*/Rule*'))
def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                if not os.path.exists(dstname):
                    copytree(srcname, dstname, symlinks, ignore)
            else:
                if not os.path.exists(dstname):
                    copy2(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except Error as err:
            errors.extend(err.args[0])

def copy_ets_reports(src, dst):
    copy2(src, dst)

def decompress_reports(src, dst):
    program_path=r'"C:\Program Files\7-zip\7z.exe"'
    output_path=" -o" + dst
    command_line = program_path + " x " + src + " -o" + dst + " -y"
    print command_line
    s=subprocess.call(command_line)

def remove_reports(dst):
    shutil.rmtree(dst, ignore_errors=True)

def copy_ingestor_reports(src,dst,file):
    program_path=r'"E:\Power\WinSCP-5.13.1-Portable\WinSCP.com"'
    #get_report=r"
    command_1=r' "open sftp://root:notwest@10.52.154.215/ -hostkey=""ssh-rsa 2048 R2gQNIT8CDWrP0q8hb6MN5t0OlwqDrkgnd6kRVr0f+Y="' + r'""'
    command_2=r' "' + "cd %s" %(src) + r'"'
    command_3=r' "' + "get %s %s" %(file,dst) + r'"'
    command_4=r' "exit""'
    command_line = program_path + " /ini=nul" + " /command" + command_1 + command_2 + command_3 + command_4
    print command_line
    s=subprocess.call(command_line)

if __name__ == "__main__":
    for x in range (1,3):
        ets_report_dir1=sys.argv[1]
        ets_report_dir=ets_report_dir1+"_%d" %(x) + "." + "zip"
        ets_report_src_dir1="X:\P%d" %(x)
        ets_report_src_dir=os.path.join(ets_report_src_dir1,ets_report_dir)
        print "ets_report_src_dir is %s" %(ets_report_src_dir)
        ets_report_dst_dir1="E:\Power\ETSReports\P%d" %(x)
        ets_report_dst_dir=os.path.join(ets_report_dst_dir1,ets_report_dir)
        print "To remove ets_report_dst_dir is %s" %(ets_report_dst_dir1)
        remove_reports(ets_report_dst_dir1)
        if not os.path.exists(ets_report_dst_dir1):
            os.makedirs(ets_report_dst_dir1)
        print "To copy and decompress ets_report_dst_dir is %s" %(ets_report_dst_dir)
        copy_ets_reports(ets_report_src_dir, ets_report_dst_dir)
        decompress_reports(ets_report_dst_dir, ets_report_dst_dir1)
        
        ingestor_report_dir1=sys.argv[2]
        ingestor_report_dir=ingestor_report_dir1+"_%d" %(x) + "." + "tar.gz"
        ingestor_report_src_dir1="/data/collectionrecovery/FeedJournalAnalyzer/report/P%d" %(x)
        ingestor_report_src_dir=os.path.join(ingestor_report_src_dir1,ingestor_report_dir)
        print "ingestor_report_src_dir is %s" %(ingestor_report_src_dir)
        ingestor_report_dst_dir1="E:\Power\IngestorReports\P%d" %(x)
        ingestor_report_dst_dir=os.path.join(ingestor_report_dst_dir1,ingestor_report_dir)
        print "To remove ingestor_report_dst_dir is %s" %(ingestor_report_dst_dir1)
        remove_reports(ingestor_report_dst_dir1)
        if not os.path.exists(ingestor_report_dst_dir1):
            os.makedirs(ingestor_report_dst_dir1)
        print "To copy and decompress ingestor_report_dst_dir is %s" %(ingestor_report_dst_dir)
        copy_ingestor_reports(ingestor_report_src_dir1, ingestor_report_dst_dir, ingestor_report_dir)
        decompress_reports(ingestor_report_dst_dir, ingestor_report_dst_dir1)
        ingestor_report_dir_tar=ingestor_report_dir1+"_%d" %(x) + "." + "tar"
        ingestor_report_dst_dir_tar=os.path.join(ingestor_report_dst_dir1,ingestor_report_dir_tar)
        decompress_reports(ingestor_report_dst_dir_tar, ingestor_report_dst_dir1)