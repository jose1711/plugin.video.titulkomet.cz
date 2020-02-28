# -*- coding: UTF-8 -*-
# /*
# *      Copyright (C) 2017 BrozikCZ
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */
import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import util
import xbmcprovider
import xbmcutil
import resolver
import utmain
from provider import ResolveException

__scriptid__ = 'plugin.video.titulkomet.cz'
__scriptname__ = 'titulkomet.cz'
__addon__ = xbmcaddon.Addon(id=__scriptid__)
__language__ = __addon__.getLocalizedString
__settings__ = __addon__.getSetting

sys.path.append(os.path.join(__addon__.getAddonInfo('path'), 'resources', 'lib'))
import titulkomet
settings = {'downloads': __addon__.getSetting('downloads'), 'quality': __addon__.getSetting('quality')}


class TitulkometXBMCContentProvider(xbmcprovider.XBMCMultiResolverContentProvider):
    def play(self, item):
        stream = self.resolve(item['url'])[0]
        if stream:
            xbmcutil.reportUsage(self.addon_id, self.addon_id + '/play')
            if 'headers' in stream.keys():
                for header in stream['headers']:
                    stream['url'] += '|%s=%s' % (header, stream['headers'][header])
            print 'Sending %s to player' % stream['url']
            li = xbmcgui.ListItem(path=stream['url'], iconImage='DefaulVideo.png')
            sub = False
            if xbmcaddon.Addon('xbmc.addon').getAddonInfo('version') > "16":
                sub = True
                if stream['subs'] is not None and stream['subs'] != '':
                    li.setSubtitles([stream['subs']])
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
            if not sub:
                xbmcutil.load_subtitles(stream['subs'])

    def resolve(self, url):
        item = self.provider.video_item()
        item.update({'url': url})

        host = 'titulkomet.cz'
        tc = 'UA-110229735-1'
        try:
            utmain.main({'id': __scriptid__, 'host': host, 'tc': tc, 'action': url})
        except:
            pass

        try:
            return self.provider.resolve(item)
        except ResolveException, e:
            self._handle_exc(e)

params = util.params()
if params == {}:
	xbmcutil.init_usage_reporting(__scriptid__)
TitulkometXBMCContentProvider(titulkomet.TitulkometContentProvider(tmp_dir=xbmc.translatePath(__addon__.getAddonInfo('profile')), quality=__addon__.getSetting('quality')), settings, __addon__).run(params)
