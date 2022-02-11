# captionPlayer
The caption player is an application that can help someone to study language. It supports *.srt or *.ass subtitle file. If mp3 file that is the same name with subtitle file, the caption player will find the start and end time of each sentence and play. 
<br>
![captionPlayer](doc/captionPlayerPic.png?raw=true "captionPlayer")
<br>

# for developer
It has to install the following module:
* pyinstaller
* pysrt
* asstosrt
* (charset)
* pygame
* gTTS

source code of asstosrt has to remove '\r'
<br>
* L.74<br>
return u'{} --> {}\r\n{}\r\n'.format(self.time_from,<br>
=><br>
return u'{} --> {}\n{}\n'.format(self.time_from,<br>

* L.132<br>
text = text.replace(r'\N', '\r\n').replace(r'\n', '\r\n')<br>
=><br>
text = text.replace(r'\N', '\n').replace(r'\n', '\n')<br>

* L.144<br>
srt += u'{}\r\n{}\r\n'.format(i, unicode(dialogue))<br>
=><br>
srt += u'{}\n{}\n'.format(i, unicode(dialogue))<br>

# for user
