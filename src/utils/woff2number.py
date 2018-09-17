# -*- coding: utf-8 -*-
# create by Aramis

import xml.sax
import requests
from fontTools import ttLib

d = {}
maoyan_woff_list = None


class AramisHandler(xml.sax.ContentHandler):

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        # print('in in in :', tag, attributes)
        if tag == 'aramis':
            d['aramis'] = []
        elif tag == 'TTGlyph':
            d['aramis'].append({'name': attributes['name'], 'contour': {}})
        elif tag == 'contour':
            d['aramis'][len(d['aramis']) - 1]['contour'] = {
                'count': attributes['count'],
                'pts': []
            }
        elif tag == 'pt':
            d['aramis'][len(d['aramis']) - 1]['contour']['pts'].append({
                'x': attributes['x'],
                'y': attributes['y'],
                'on': attributes['on']
            })
        else:
            pass


class AramisSimpleHandler(xml.sax.ContentHandler):
    last_name = ''

    def startElement(self, name, attrs):
        if name == 'aramis':
            d['aramis'] = []
        elif name == 'TTGlyph':
            self.last_name = attrs['name']
            d['aramis'].append({attrs['name']: []})
        elif name == 'contour':
            d['aramis'][len(d['aramis']) - 1][self.last_name].append(attrs['count'])
        else:
            pass


class WoffHandler(xml.sax.ContentHandler):

    def startElement(self, name, attrs):
        if name == 'glyf':
            d['glyf'] = []
        elif name == 'TTGlyph':
            d['glyf'].append({'name': attrs['name'], 'contours': []})
        elif name == 'contour':
            # {'count': 0, 'pts': []}
            d['glyf'][len(d['glyf']) - 1]['contours'].append({'count': 0, 'pts': []})
        elif name == 'pt':
            contours = d['glyf'][len(d['glyf']) - 1]['contours']
            count = contours[len(contours) - 1]['count']
            contours[len(contours) - 1]['count'] = count + 1
            contours[len(contours) - 1]['pts'].append({'x': attrs['x'], 'y': attrs['y'], 'on': attrs['on']})


def parse_woff_simple(path: str):
    r = _parse(path, WoffHandler())
    r_l = []
    s = {
        21: 0,
        13: 1,
        37: 2,
        44: 3,
        11: 4,
        32: 5,
        33: 6,
        20: 7,
        36: 9,
    }
    for i in r['glyf']:
        if i['contours']:
            r_d = {'name': None, 'contour_count': []}
            name = i['name']
            r_d['name'] = name
            r_d['name_n'] = name[3:]
            for j in i['contours']:
                if len(i['contours']) == 3:
                    r_d['value'] = 8
                else:
                    r_d['value'] = s.get(int(i['contours'][0]['count']), -1)
                r_d['contour_count'].append(j['count'])
            r_l.append(r_d)

    r_l.sort(key=lambda x: x['value'])

    return r_l


def parse_woff(path: str):
    return _parse(path, WoffHandler())


def parse(path: str):
    return _parse(path, AramisHandler())


def parse_simple(path: str):
    return _parse(path, AramisSimpleHandler())


def _parse(path: str, handler):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(handler)
    parser.parse(path)
    return d


def parse2num_str(s: str, filepath='../temp/current.xml'):
    woff_list = parse_woff_simple(filepath)

    return _parse2num(s, woff_list)


def parse_list2num_str(l: list, filepath: str = '../temp/current.xml'):
    if maoyan_woff_list:
        woff_list = maoyan_woff_list
    else:
        woff_list = parse_woff_simple(filepath)
    return [_parse2num(i, woff_list) for i in l if i]


def _parse2num(s: str, woff_list):
    r_str = ''
    for i in s.split(';'):
        if len(i) > 3:
            con = False
            if '.' in i:
                con = True
                xs = i[4:]
            else:
                xs = i[3:]
            if con:
                r_str += '.'
            for j in woff_list:
                if j['name_n'].lower() == xs:
                    r_str += str(j['value'])

    return r_str


def save_font(font_url: str):
    if font_url:
        font_res = requests.get(font_url)
        if font_res.status_code == 200:
            with open('../temp/current.woff', 'wb') as f:
                f.write(font_res.content)
            font = ttLib.TTFont('../temp/current.woff')
            font.saveXML('../temp/current.xml')
            print('保存字体xml成功')
            maoyan_woff_list = parse_woff_simple('../temp/current.xml')


if __name__ == '__main__':
    num_o = '&#xf03a;&#xf687;&#xf858;&#xee18;.&#xf858;'

    w2n = parse2num_str(num_o, 'current.xml')
    print(w2n)

    l = ['&#xf7cd;&#xeda0;&#xec20;&#xe8a0;.&#xec20;', '&#xe740;&#xe2cd;&#xe2cd;.&#xe5b9;',
         '&#xedbe;&#xe2cd;&#xe3a9;.&#xe2cd;', '&#xec20;&#xeda0;&#xedbe;.&#xe2cd;', '&#xec20;&#xe5b9;&#xf7cd;.&#xf7cd;',
         '&#xec20;&#xe8a0;&#xe740;.&#xe740;', '&#xe5b9;&#xe740;&#xe8a0;.&#xe5b9;', '&#xe5b9;&#xe3a9;&#xe5b9;.&#xe3a9;',
         '&#xe5b9;&#xec20;&#xe3a9;.&#xe2cd;', '&#xe740;&#xe2cd;.&#xeda0;']

    w2nl = parse_list2num_str(l, 'current.xml')
    print(w2nl)
