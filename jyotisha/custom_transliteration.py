#!/usr/bin/python3
#  -*- coding: utf-8 -*-

import logging
import re

from indic_transliteration import sanscript, language_code_to_script

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)


def romanise(iast_text):
  swapTable = {'ā': 'a', 'Ā': 'A', 'ī': 'i', 'ū': 'u', 'ê': 'e', 'ṅ': 'n', 'ṇ': 'n',
               'ḍ': 'd', 'ṭ': 't', 'ṃ': 'm', 'ñ': 'n', 'ṉ': 'n', 'ṛ': 'ri', 'ś': 'sh',
               'Ś': 'Sh', 'ṣ': 'sh', 'Ṣ': 'Sh', 'ḥ': '', '-': '-', ' ': '-'}

  roman_text = ''
  for char in iast_text:
    if char in swapTable:
      roman_text += swapTable[char]
    else:
      roman_text += char
  return roman_text.lower()


def tr(text, script, titled=True, source_script=sanscript.roman.HK_DRAVIDIAN):
  """
  
  NOTE: Please don't put your custom tex/ md/ ics whatever code here and pollute core library functions. Wrap this in your own functions if you must. Functions should be atomic."""
  if script == 'hk':
    script = sanscript.roman.HK_DRAVIDIAN
  if text == '':
    return ''
  # TODO: Fix this ugliness.
  t = text.replace('~', '##~##')  # Simple fix to prevent transliteration of ~
  transliterated_text = sanscript.transliterate(data=t, _from=source_script, _to=script).replace('C', 'Ch').replace('c', 'ch')
  if titled:
    transliterated_text = transliterated_text.title()
        # for sep in [' ', '\t', '\n']:
    #   text_parts = transliterated_text.split(sep)
    #   if len(text_parts) > 1:
    #     new_transliterated_text = ''
    #     for x in text_parts:
    #       if len(x) > 1:
    #         transliterated_text = sep.join([(x[0].upper() + x[1:]) for x in text_parts])
    #       else:

  if script == sanscript.TAMIL:
    transliterated_text = sanscript.SCHEMES[sanscript.TAMIL].apply_roman_numerals(transliterated_text)
    # transliterated_text = clean_tamil_Na(transliterated_text)
  if script.startswith('iast'):
    transliterated_text = transliterated_text.replace('ṉ', 'n')
    caret_accent = '̂'
    for _match in re.findall(caret_accent + '.', transliterated_text):
      transliterated_text = transliterated_text.replace(_match, _match.lower())
  if script == 'telugu' or script == sanscript.TELUGU:
    transliterated_text = transliterated_text.replace('ऩ', 'న')
  return transliterated_text


def sexastr2deci(sexa_str):
  """Converts as sexagesimal string to decimal

  Converts a given sexagesimal string to its decimal value

  Args:
    A string encoding of a sexagesimal value, with the various
    components separated by colons

  Returns:
    A decimal value corresponding to the sexagesimal string

  Examples:
    >>> sexastr2deci('15:30:00')
    15.5
    >>> sexastr2deci('-15:30:45')
    -15.5125
  """

  if sexa_str[0] == '-':
    sgn = -1.0
    dms = sexa_str[1:].split(':')  # dms = degree minute second
  else:
    sgn = 1.0
    dms = sexa_str.split(':')

  decival = 0
  for i in range(0, len(dms)):
    decival = decival + float(dms[i]) / (60.0 ** i)

  return decival * sgn


def print_lat_lon(lat, lon):
  """Returns a formatted string for a latitude and longitude

  Returns a formatted string for latitude and longitude, given sexagesimal
  'strings' using colons for separation

  Args:
    str latstr
    str lonstr

  Returns:
    string corresponding to the formatted latitude and longitude

  Examples:
    >>> print_lat_lon('13:05:24','80:16:12') #Chennai
    "13°05'24''N, 80°16'12''E"
    >>> print_lat_lon('37:23:59','-122:08:34') #Palo Alto
    "37°23'59''N, 122°08'34''W"
    >>> print_lat_lon(1, -1)
    "1°0'0''N, 1°0'0''W"
  """

  if lat < 0:
    lat = -lat
    lat_suffix = 'S'
  else:
    lat_suffix = 'N'

  if lon < 0:
    lon = -lon
    lon_suffix = 'W'
  else:
    lon_suffix = 'E'

  return '%.3f°%s, %.3f°%s' % (lat, lat_suffix, lon, lon_suffix)


def clean_tamil_Na(text):
  output_text = re.sub('([^ ])ந', '\\1ன', text)
  output_text = re.sub('([-—*])ன', '\\1ந', output_text)
  output_text = re.sub('ன்த', 'ந்த', output_text)
  return output_text


def transliterate_from_language(text, language, script):
  if language == "ta":
    # Tamil names are stored in HK (because the latter differentiates between vargIya consonants!)
    transliterated_text = tr(text, script)
  else:
    source_script = language_code_to_script[language]
    transliterated_text = sanscript.transliterate(text, source_script, script)
  return transliterated_text

