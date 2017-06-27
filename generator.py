#!/usr/bin/python3

import argparse
import json
import os.path
import shutil
import sys

from jinja2 import Template


parser = argparse.ArgumentParser(
    description='Generate C++ files using a template file and a configuration')
parser.add_argument('--cfg', metavar='PATH', type=str, nargs='+',
                    help='path to the configuration files to be used')
parser.add_argument('--files', metavar='FILES', type=str, nargs='+',
                    default=['templates/Structures', 'templates/Converter'],
                    help='one (or more) template files to be processed')
parser.add_argument('--output', type=str, default='./generated/', nargs='?',
                    help='the directory in which the new files get created')


args = parser.parse_args()

projectPath = os.path.dirname(sys.argv[0])
path = os.path.join(projectPath, 'jsonserializer')
sources = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

written = 0
files = [os.path.join(projectPath, f) for f in args.files]
output = args.output
headers = []


if os.path.isdir(output):
    shutil.rmtree(output)
os.mkdir(output)
for f in sources:
    _, ext = os.path.splitext(f)
    if ext == 'h':
        headers.append(f)
    shutil.copy(f, output)
    
for cfgFile in args.cfg:
    if not os.path.exists(cfgFile):
        print('Configuration file not found! Skipping.')
        continue

    with open(cfgFile) as f:
        cfg = json.loads(f.read())

    # set default values
    for struct in cfg['structures']:
        if 'transient' not in struct:
            struct['transient'] = False
        if 'namespace' not in struct:
            struct['namespace'] = 'structures'

        for field in struct['fields']:
            if 'ccname' not in field:
                field['ccname'] = field['name'].title()
            if 'required' not in field:
                field['required'] = False
            if 'type' not in field:
                field['type'] = 'int'

    if 'name' in cfg:
        prefix = cfg['name']
    else:
        prefix = ''

    for templateFile in files:
        hFile = templateFile + '.h'
        if not os.path.exists(hFile):
            print('Template header file "' + hFile + '" not found! Skipping.')
            continue

        headers.append(hFile)
        name = os.path.join(output,
                            prefix + os.path.basename(hFile))
        with open(hFile) as f:
            content = Template(f.read()).render(cfg)

        with open(name, 'w') as f:
            f.write(content)

        print('Wrote header file "' + name + '"')
        written = written + 1

        cppFile = templateFile + '.cpp'
        if not os.path.exists(cppFile):
            print('Template source file "' + cppFile + '" not found! Skipping.')
            continue

        cfg['header'] = os.path.basename(name)
        name = os.path.join(output,
                            prefix + os.path.basename(cppFile))
        with open(cppFile) as f:
            content = Template(f.read()).render(cfg)

        with open(name, 'w') as f:
            f.write(content)

        print('Wrote source file "' + name + '"')
        written = written + 1


print('')
print('Successfully written ' + str(written) +
      ' out of ' + str(len(args.files) * 2 * len(args.cfg)) + ' files.')
