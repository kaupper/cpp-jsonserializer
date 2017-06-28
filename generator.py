#!/usr/bin/python3

import argparse
import json
import os.path
import shutil
import sys
import re

from jinja2 import Template


parser = argparse.ArgumentParser(
    description='Generate C++ files using a configuration file')
parser.add_argument('--cfg', metavar='PATH', type=str, nargs='+',
                    help='path to the configuration files to be used')


args = parser.parse_args()

projectPath = os.path.dirname(sys.argv[0])
path = os.path.join(projectPath, 'jsonserializer')
sources = [os.path.join(path, f) for f in os.listdir(
    path) if os.path.isfile(os.path.join(path, f))]

path = os.path.join(projectPath, 'templates')
files = ['Structures', 'Converter']
files = [os.path.join(path, f) for f in files]

written = 0
headers = []

outputHeader = os.path.join(projectPath, 'generated-inc', 'jsonserializer')
outputSrc = os.path.join(projectPath, 'generated-src')

# prepare file system
if os.path.isdir(outputHeader):
    shutil.rmtree(outputHeader)
if os.path.isdir(outputSrc):
    shutil.rmtree(outputSrc)
os.makedirs(outputHeader)
os.makedirs(outputSrc)
for f in sources:
    _, ext = os.path.splitext(f)
    if ext == '.h':
        headers.append(f)
        shutil.copy(f, outputHeader)
    else:
        shutil.copy(f, outputSrc)


def checkConfigurationFile(cfg):
    def typeError(msg):
        print('')
        print('TypeError: ' + msg)
        print('')
        exit(1)

    # name
    if 'name' not in cfg:
        cfg['name'] = ''
    if not isinstance(cfg['name'], str):
        typeError('"name" has to be a string!')

    # global_includes
    if 'global_includes' not in cfg:
        cfg['global_includes'] = []
    if not isinstance(cfg['global_includes'], list):
        typeError('"global_includes" has to be an array!')

    for inc in cfg['global_includes']:
        if not isinstance(inc, str):
            typeError('entries of "global_includes" have to be strings!')

    # local_includes
    if 'local_includes' not in cfg:
        cfg['local_includes'] = []
    if not isinstance(cfg['local_includes'], list):
        typeError('"local_includes" has to be an array!')
    for inc in cfg['local_includes']:
        if not isinstance(inc, str):
            typeError('entries of "local_includes" have to be strings!')

    # namespace
    if 'namespace' not in cfg:
        cfg['namespace'] = 'structures'
    if not isinstance(cfg['namespace'], str):
        typeError('"namespace" has to be a string!')

    # structures
    if 'structures' not in cfg:
        cfg['structures'] = []
    if not isinstance(cfg['structures'], list):
        typeError('"structures" has to be an array!')

    for struct in cfg['structures']:
        # structures.name
        if 'name' not in struct:
            typeError('"structures.name" must not be empty!')
        if not isinstance(struct['name'], str):
            typeError('"structures.name" has to be a string!')

        # structures.transient
        if 'transient' not in struct:
            struct['transient'] = False
        if not isinstance(struct['transient'], bool):
            typeError('"structures.transient" has to be a boolean!')

        # structures.fields
        if 'fields' not in struct:
            struct['fields'] = []
        if not isinstance(struct['fields'], list):
            typeError('"structures.fields" has to be an array!')

        for field in struct['fields']:
            # structures.fields.name
            if 'name' not in field:
                typeError('"structures.fields.name" must not be empty!')
            if not isinstance(field['name'], str):
                typeError('"structures.fields.name" has to be a string!')

            # structures.fields.ccName
            if 'ccName' not in field:
                field['ccName'] = field['name'][0].upper() + field['name'][1:]
            if not isinstance(field['ccName'], str):
                typeError('"structures.fields.ccName" has to be a string!')

            # structures.fields.jsonName
            if 'jsonName' not in field:
                tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', field['ccName'])
                field['jsonName'] = re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp) \
                                      .lower()
            if not isinstance(field['jsonName'], str):
                typeError(
                    '"structures.fields.jsonName" has to be a string!')
                exit(1)

            # structures.fields.type
            if 'type' not in field:
                field['type'] = 'int'
            if not isinstance(field['type'], str):
                typeError('"structures.fields.type" has to be a string!')

            # structures.fields.required
            if 'required' not in field:
                field['required'] = False
            if not isinstance(field['required'], bool):
                typeError(
                    '"structures.fields.required" has to be a boolean!')
                exit(1)


for cfgFile in args.cfg:
    if not os.path.exists(cfgFile):
        print('Configuration file not found! Skipping.')
        continue

    with open(cfgFile) as f:
        cfg = json.loads(f.read())

    checkConfigurationFile(cfg)
    prefix = cfg['name']

    for templateFile in files:
        hFile = templateFile + '.h'
        if not os.path.exists(hFile):
            print('Template header file "' + hFile + '" not found! Skipping.')
            continue

        headers.append(hFile)
        name = os.path.join(outputHeader,
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
        name = os.path.join(outputSrc,
                            prefix + os.path.basename(cppFile))
        with open(cppFile) as f:
            content = Template(f.read()).render(cfg)

        with open(name, 'w') as f:
            f.write(content)

        print('Wrote source file "' + name + '"')
        written = written + 1


print('')
print('Successfully written ' + str(written) +
      ' out of ' + str(len(files) * 2 * len(args.cfg)) + ' files.')
