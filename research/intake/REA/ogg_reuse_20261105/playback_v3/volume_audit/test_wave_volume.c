#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <mmsystem.h>
#include <stdio.h>
int main(void){
 WAVEFORMATEX f={WAVE_FORMAT_PCM,2,44100,176400,4,16,0};
 HWAVEOUT a=0,b=0;DWORD av=0,bv=0,after=0;MMRESULT r;int rc=0,changed=0;
 r=waveOutOpen(&a,WAVE_MAPPER,&f,0,0,CALLBACK_NULL);if(r)return 2;
 r=waveOutOpen(&b,WAVE_MAPPER,&f,0,0,CALLBACK_NULL);if(r){waveOutClose(a);return 3;}
 if(waveOutGetVolume(a,&av)||waveOutGetVolume(b,&bv)){rc=4;goto done;}
 printf("BEFORE first=%08lx second=%08lx\n",(unsigned long)av,(unsigned long)bv);
 r=waveOutSetVolume(a,0x0ccc0cccu);if(r){rc=5;goto done;}changed=1;
 r=waveOutGetVolume(b,&after);if(r){rc=6;goto done;}
 printf("AFTER_SET_FIRST second=%08lx shared_effect=%d\n",(unsigned long)after,after==0x0ccc0cccu);
done:
 if(changed){r=waveOutSetVolume(a,av);printf("RESTORE_FIRST result=%u\n",r);if(r)rc=7;}
 waveOutClose(b);waveOutClose(a);return rc;
}
