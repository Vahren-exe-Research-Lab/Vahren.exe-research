#define COBJMACROS
#define DIRECTSOUND_VERSION 0x0800
#include <windows.h>
#include <dsound.h>
#include <stdio.h>
#include <string.h>
#define main volume_audit_main
#include "read_session_volume.c"
#undef main
int main(void){
 IDirectSound8 *ds=0;IDirectSoundBuffer *a=0,*b=0;int rc=1;HRESULT hr;LONG av,bv;
 HWND window=CreateWindowExW(0,L"STATIC",L"OGG silent volume test",WS_POPUP,0,0,1,1,0,0,GetModuleHandleW(0),0);
 if(!window)return 2;
 WAVEFORMATEX f={WAVE_FORMAT_PCM,2,44100,176400,4,16,0};
 DSBUFFERDESC desc={0};desc.dwSize=sizeof desc;desc.dwFlags=DSBCAPS_CTRLVOLUME|DSBCAPS_GLOBALFOCUS|DSBCAPS_LOCSOFTWARE;desc.dwBufferBytes=17640;desc.lpwfxFormat=&f;
 hr=DirectSoundCreate8(0,&ds,0);if(FAILED(hr))goto done;
 hr=IDirectSound8_SetCooperativeLevel(ds,window,DSSCL_NORMAL);if(FAILED(hr))goto done;
 hr=IDirectSound8_CreateSoundBuffer(ds,&desc,&a,0);if(FAILED(hr))goto done;
 hr=IDirectSound8_CreateSoundBuffer(ds,&desc,&b,0);if(FAILED(hr))goto done;
 IDirectSoundBuffer *buffers[]={a,b};
 for(int i=0;i<2;i++){void *p=0,*q=0;DWORD n=0,m=0;
 hr=IDirectSoundBuffer_Lock(buffers[i],0,desc.dwBufferBytes,&p,&n,&q,&m,0);if(FAILED(hr))goto done;
 memset(p,0,n);if(q)memset(q,0,m);
 hr=IDirectSoundBuffer_Unlock(buffers[i],p,n,q,m);if(FAILED(hr))goto done;
 hr=IDirectSoundBuffer_Play(buffers[i],0,0,DSBPLAY_LOOPING);if(FAILED(hr))goto done;}
 char pid[32];snprintf(pid,sizeof pid,"%lu",(unsigned long)GetCurrentProcessId());char *args[]={"audit",pid};
 puts("DS_BEFORE");volume_audit_main(2,args);
 hr=IDirectSoundBuffer_GetVolume(a,&av);if(FAILED(hr))goto done;hr=IDirectSoundBuffer_GetVolume(b,&bv);if(FAILED(hr))goto done;
 printf("BUFFER_BEFORE first=%ld second=%ld\n",av,bv);
 hr=IDirectSoundBuffer_SetVolume(a,-3000);if(FAILED(hr))goto done;
 hr=IDirectSoundBuffer_GetVolume(a,&av);if(FAILED(hr))goto done;hr=IDirectSoundBuffer_GetVolume(b,&bv);if(FAILED(hr))goto done;
 printf("BUFFER_AFTER first=%ld second=%ld\n",av,bv);
 puts("DS_AFTER");volume_audit_main(2,args);
 rc=(av==-3000&&bv==0)?0:3;
done:
 printf("DS_RESULT=%d hr=%08lx\n",rc,(unsigned long)hr);
 if(b){IDirectSoundBuffer_Stop(b);IDirectSoundBuffer_Release(b);}if(a){IDirectSoundBuffer_Stop(a);IDirectSoundBuffer_Release(a);}
 if(ds)IDirectSound8_Release(ds);DestroyWindow(window);return rc;
}
