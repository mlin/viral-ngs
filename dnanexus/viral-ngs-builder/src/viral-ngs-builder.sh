#!/bin/bash

main() {
    set -e -x -o pipefail

    # record a manifest of the filesystem before doing anything
    (find / -type f 2> /dev/null || true) | sort > /tmp/fs-manifest.0

    # clone viral-ngs
    git clone -n "$git_url" viral-ngs
    cd viral-ngs
    git checkout "$git_commit"
    GIT_REVISION=$(git describe --long --tags --dirty --always)

    # build viral-ngs
    pip install $(cat requirements.txt | grep -iv numpy | grep -iv scipy | grep -iv cython)
    ./run_all_tests.sh

    # record a new filesystem manifest
    (find / -type f 2> /dev/null || true) | sort > /tmp/fs-manifest.1

    # diff the two manifests to get a list of all new files
    comm -1 -3 /tmp/fs-manifest.0 /tmp/fs-manifest.1 | \
      egrep -v "^/proc" | egrep -v "^/sys" | egrep -v "^/tmp" | egrep -v "/\.git/" \
      > /tmp/resources-manifest.txt

    # upload a tarball with the new files
    resources=`tar -c -v -z -T /tmp/resources-manifest.txt | \
               dx upload --brief -o "viral-ngs-${GIT_REVISION}.resources.tar.gz" -`

    dx-jobutil-add-output resources "$resources" --class=file
}
