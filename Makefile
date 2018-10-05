# This is needed only for *compiling* the dotstar.so file (Python module).
# Not needed for just running the Python code with a precompiled .so file.

# Usage
#
# make - Uses the default Python version which is currently 3.6
# make python3.5 - Uses the Python 3.5 version headers
# make python3.6 - Uses the Pyton 3.6 version headers
# make clean - Removes all build output
 
DEFINES=-D__PYTHON_H__="<python3.6m/Python.h>"

all: dotstar.so

python3.5: DEFINES=-D__PYTHON_H__="<python3.5/Python.h>"
python3.5: all

python3.6: DEFINES=-D__PYTHON_H__="<python3.6m/Python.h>"
python3.6: all

CFLAGS=-Ofast -fomit-frame-pointer \
	-I/opt/vc/include \
	-I/usr/local/include \
	-L/opt/vc/lib

dotstar.so: dotstar.o
	gcc -s -shared -Wl,-soname,libdotstar.so,-L/opt/vc/lib,-lbcm_host -o $@ $<

.c.o:
	gcc $(CFLAGS) $(DEFINES) -c $<

clean:
	rm -f dotstar.o dotstar.so
