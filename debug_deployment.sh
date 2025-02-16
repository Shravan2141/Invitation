#!/bin/bash

# Extensive system and Python environment debugging

echo "SYSTEM INFORMATION:"
echo "----------------"
uname -a
cat /etc/os-release

echo -e "\nPYTHON ENVIRONMENT:"
echo "-------------------"
which python
python --version
python -c "import sys; print(sys.executable)"

echo -e "\nPIP INFORMATION:"
echo "----------------"
pip --version
pip list

echo -e "\nTRYING PIP INSTALL WITH VERBOSE OUTPUT:"
echo "----------------------------------------"
pip install --verbose -r src/requirements.txt

echo -e "\nFINAL PIP FREEZE:"
echo "-----------------"
pip freeze

# If everything fails, output a failure message
exit 1
