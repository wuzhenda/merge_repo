#!/usr/bin/env python
import os
import sys
import urllib2
import json
import re
from xml.etree import ElementTree


def get_from_manifest(manifest_name):
    try:
        lm = ElementTree.parse(manifest_name)
        lm = lm.getroot()
    except:
        lm = ElementTree.Element("manifest")

    proj=lm.findall("project")
    return proj 


def add_to_manifest(out_manifest,projects):
    try:
        lm = ElementTree.parse(manifest_name)
        lm = lm.getroot()
    except:
        lm = ElementTree.Element("manifest")

    for proj in  projects:
        lm.append(proj)
    raw_xml = ElementTree.tostring(lm)
    raw_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + raw_xml

    f = open(out_manifest, 'w')
    f.write(raw_xml)
    f.close()


cwd = os.path.abspath( os.path.dirname( __file__ ) )
manifest_dir = os.path.join( cwd,'manifest_dir')
out_manifest_dir = os.path.join( cwd,'out_manifest_dir')

local_manifest=os.path.join(manifest_dir,"cb_manifest.xml")
aosp_manifest=os.path.join(manifest_dir,"aosp_manifest.xml")
out_same_manifest=os.path.join(out_manifest_dir,"out_same_manifest.xml")
out_local_manifest=os.path.join(out_manifest_dir,"out_local_manifest.xml")
out_aosp_manifest=os.path.join(out_manifest_dir,"out_aosp_manifest.xml")

local_proj=get_from_manifest(local_manifest)
aosp_proj=get_from_manifest(aosp_manifest)

same_proj=[]
onlylocal_proj=[]
onlyaosp_proj=[]

for l_proj in local_proj:
    haveIt=False
    for a_proj in aosp_proj:
        if  l_proj.get("path") == a_proj.get("path"):
            haveIt=True
            same_proj.append(a_proj)
            break
    if not haveIt:
        print("local have only %s ")%(l_proj.get("name"))
        onlylocal_proj.append(l_proj)

for a_proj in aosp_proj:
    if not a_proj in same_proj:
        onlyaosp_proj.append(a_proj)
    

add_to_manifest(out_same_manifest,same_proj)
add_to_manifest(out_local_manifest,onlylocal_proj)
add_to_manifest(out_aosp_manifest,onlyaosp_proj)
