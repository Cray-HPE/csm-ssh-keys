#!/bin/bash

# Copyright 2021 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# (MIT License)

# Very simple scanner for files missing copyrights & licenses

# Extensions to check
CODE_EXTENSIONS="py sh spec"

# Additional files to check, uses exact match
EXTRA_FILES="Dockerfile"
# We also want to check the ansible yaml files
while read F ; do
    EXTRA_FILES="$EXTRA_FILES $F"
done << $(find ansible -type f \( -iname \*.yml -o -iname \*.yaml \) -print)

WHITELIST_FILES=""

FAIL=0

function scan_file {
    echo -n "Scanning $1... "
    # skip empty files
    if [ -s $1 ]; then
        grep -q "Copyright" $1
        if [ $? -ne 0 ]; then
            echo "missing copyright headers"
            return 1
        fi
        grep -q "MIT License" $1
        if [ $? -ne 0 ]; then
            echo "missing MIT license"
            return 1
        fi
    fi
    echo "OK"
    return 0
}

function list_include_item {
  local list="$1"
  local item="$2"
  if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]] ; then
    # yes, list include item
    result=0
  else
    result=1
  fi
  return $result
}

# Scan extensions
for CE in ${CODE_EXTENSIONS}
do
    for F in `git ls-files "*.${CE}"`
    do
        if ! list_include_item "$WHITELIST_FILES" "$F"; then
            scan_file ${F} || FAIL=1
        fi
    done
done

# Do the listed extra files
for F in ${EXTRA_FILES}
do
    if ! list_include_item "$WHITELIST_FILES" "$F"; then
        scan_file ${F} || FAIL=1
    fi
done

if [ ${FAIL} -eq 0 ]; then
    echo "All scanned code passed"
else
    echo "Some code is missing copyright or license, see list above"
fi

exit ${FAIL}