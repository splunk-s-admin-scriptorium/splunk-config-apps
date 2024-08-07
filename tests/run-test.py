#!/usr/bin/env python

import array
import os
import argparse
import subprocess
import shutil

quiet = False
cleanup = False
project_root = None
test_id = None
test_conf= None

argparser = argparse.ArgumentParser(description = "Tests script compiling config apps for Splunk")

argparser.add_argument( "project_root", help = "Project root path")
argparser.add_argument( "test_id", help = "Test ID")

argparser.add_argument("-q", "--quiet", action='store_true', help="Quiet output")
argparser.add_argument("-c", "--cleanup", action='store_true', help="Cleanup results")

args = argparser.parse_args()

if args.quiet:
	quiet = True
if args.cleanup:
	cleanup = True
if args.project_root:
	project_root = args.project_root
if args.test_id:
	test_id = args.test_id

commpile_script = os.path.join(project_root,"utils","scripts","compile-apps.py")
apps_path = os.path.join(project_root,"apps")
apps_sources_path = os.path.join(project_root,"apps_sources")

test_path = os.path.join(project_root,"tests", "test_cases",test_id)
test_conf_json = os.path.join(test_path,"conf.json")
test_conf_yaml = os.path.join(test_path,"conf.yaml")
test_results_path = os.path.join(test_path,"_out")
test_expected_results_path = os.path.join(test_path,"expected")


if(not os.path.exists(project_root)):
	print("Project root path does not exist: "+project_root)
	print("FAIL")
	exit(1001)
if(not os.path.exists(commpile_script)):
	print("Compile script does not exist: "+commpile_script)
	print("FAIL")
	exit(1002)
if(not os.path.exists(apps_path)):
	print("Apps path does not exist: "+apps_path)
	print("FAIL")
	exit(1003)
if(not os.path.exists(apps_sources_path)):
	print("Apps Sourcest path does not exist: "+apps_sources_path)
	print("FAIL")
	exit(1004)

if(not os.path.exists(test_path)):
	print("Test case path does not exist: "+test_path)
	print("FAIL")
	exit(1011)
if(not os.path.exists(test_conf_json)):
	if(not os.path.exists(test_conf_yaml)):
		print("Test case path does not exist: "+test_conf_json)
		print("Test case path does not exist: "+test_conf_yaml)
		print("FAIL")
		exit(1012)
	else:
		test_conf = test_conf_yaml
else:
	test_conf = test_conf_json
if(not os.path.exists(test_expected_results_path)):
	print("Expected results for test case does not exist: "+test_expected_results_path)
	print("FAIL")
	exit(1013)


ret = subprocess.call(['python', commpile_script, "-q", test_conf, test_results_path, apps_path, apps_sources_path])
if (ret != 0):
	print("Compilation failed.")
	print("FAIL")
	exit (-1)

## Verification
return_code = 0
if(os.path.isdir(test_results_path)):
	for root, dirs, files in os.walk(test_results_path):
		for file in files:
			if(os.path.isfile(os.path.join(test_expected_results_path,os.path.relpath(os.path.join(root,file),test_results_path)))):
				with open(os.path.join(test_expected_results_path,os.path.relpath(os.path.join(root,file),test_results_path)), "r") as expected, open(os.path.join(root,file), "r") as result:
					i = 0
					el = expected.readlines()
					rl = result.readlines()
					for e in el:
						if (i>=len(rl)):
							print("\tUnexpected line: "+r)
							if (return_code == 0):
								return_code=1
						r=rl[i]
						if ( e != r ):
							print("Non-matching line found: "+str(i+1))
							print("\tExpected: "+e)
							print("\tReceived: "+r,end="")
							if (return_code == 0):
								return_code=1
						i += 1
					while(i < len(rl)):
						i += 1
						print("\tUnexpected line ["+str(i)+"]: "+r)
						if (return_code == 0):
							return_code=1
			else:
				print("Unexpected file in results: "+os.path.relpath(os.path.join(root,file),test_results_path))
				if (return_code == 0):
					return_code=-3
else:
	print("No results found in: " + test_results_path)
if cleanup and os.path.isdir(test_results_path):
	shutil.rmtree(test_results_path)
if return_code == 0:
	print("PASS")
else:
	print("FAIL")

exit(return_code)