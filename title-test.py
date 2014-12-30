#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import urllib2

import jbovlaste

defs = dict(jbovlaste.definitions)

def add_title(word, title):
  return u'<span title="%s">%s</span>' % (title, word)

word_re = re.compile(r"^[a-zA-Z,']+")
nonword_re = re.compile(r"^[^a-zA-Z,']+")

def process_text(text):
  output = ''
  while text != '':
    word = word_re.findall(text)
    if word:
      word = word[0]
      if word in defs:
        output += add_title(word, defs[word].decode('utf-8'))
      else:
        output += word
      text = text[len(word):]
    else:
      nonword = nonword_re.findall(text)[0]
      output += nonword
      text = text[len(nonword):]
  return output

def process_html(html):
  output = html[:html.find('<body')]
  html = html[html.find('<body'):]
  tag_re = re.compile(r'^<.*?>')
  nontag_re = re.compile(r'^[^<]+')
  while html != '':
    if html[0] == '<':
      tag = tag_re.findall(html)[0]
      output += tag
      html = html[len(tag):]
    else:
      nontag = nontag_re.findall(html)[0]
      output += process_text(nontag)
      html = html[len(nontag):]
  return output.encode('utf-8')

def process_url(url):
  return process_html(urllib2.urlopen(url).read().decode('latin1'))

import sys

if __name__ == '__main__':
  if len(sys.argv) == 2:
    print process_url(sys.argv[1])
