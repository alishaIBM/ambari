#!/usr/bin/ambari-python-wrap

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import sys
import re
from ambari_commons import OSCheck

def main(argv=None):
  # Same logic that was in "os_type_check.sh"
  if len(sys.argv) != 2:
    print "Usage: <cluster_os>"
    raise Exception("Error in number of arguments. Usage: <cluster_os>")
    pass

  cluster_os = sys.argv[1]
  current_os_family = OSCheck.get_os_family()
  current_os_version = OSCheck.get_os_major_version()
  current_os = current_os_family + current_os_version

  # If agent/server have the same {"family","main_version"} - then ok.
  print "Cluster primary/cluster OS family is %s and local/current OS family is %s" % (
    cluster_os, current_os)
  if _check_compatibility(cluster_os, current_os_family, current_os_version):
    sys.exit(0)
  else:
    raise Exception("Local OS is not compatible with cluster primary OS family. Please perform manual bootstrap on this host.")

# this method should return true to allow hybrid cluster setup
# compare cluster_os with current_os_family+current_os_version
def _check_compatibility(cluster_os, current_os_family, current_os_version):
  #get cluster os family and major version
  OS_PATTERN = "([\\D]+|(?:[\\D]+[\\d]+[\\D]+))([\\d]*)"
  m = re.match(OS_PATTERN, cluster_os)
  if m and len(m.groups()) > 1:
    cluster_os_family = m.group(1)
    cluster_os_version = m.group(2)
  else:
    cluster_os_family = cluster_os
    cluster_os_version = ""
  
  return (current_os_family in cluster_os_family or cluster_os_family in current_os_family) and (cluster_os_version == current_os_version)

if __name__ == "__main__":
  main()
