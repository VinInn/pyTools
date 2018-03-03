#!/usr/bin/env python
import tempfile
import random
import sys
if __name__ == '__main__':
    functions = list()
    for i in range(10000):
        func_name = "f_{0}".format(next(tempfile._get_candidate_names()))
        sys.stdout.write("void {0}() {{\n".format(func_name))
        sys.stdout.write("    double pi = 3.14, r = 50, h = 100, e = 2.7, res;\n")
        sys.stdout.write("    res = pi*r*r*h;\n")
        sys.stdout.write("    res = res/(e*e);\n")
        sys.stdout.write("}\n")
        functions.append(func_name)
    sys.stdout.write("int main() {\n")
    sys.stdout.write("unsigned int i;\n")
    sys.stdout.write("for(i =0 ; i < 100000 ;i ++ ){\n")
    j = 0
    for i in range(10000):
        r = random.randint(0, len(functions)-1)
        sys.stdout.write("{0}();\n".format(functions[r]))
    sys.stdout.write("}\n")
    sys.stdout.write("}\n")

