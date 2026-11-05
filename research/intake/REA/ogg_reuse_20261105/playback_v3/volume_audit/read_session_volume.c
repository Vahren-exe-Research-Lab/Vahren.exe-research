#define COBJMACROS
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <initguid.h>
#include <mmdeviceapi.h>
#include <audiopolicy.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char**argv){
 if(argc!=2)return 2;DWORD wanted=strtoul(argv[1],0,10);if(!wanted)return 2;
 HRESULT hr=CoInitializeEx(0,COINIT_MULTITHREADED);if(FAILED(hr))return 3;
 IMMDeviceEnumerator *enumerator=0;IMMDeviceCollection *devices=0;UINT device_count=0;unsigned matches=0;
 hr=CoCreateInstance(&CLSID_MMDeviceEnumerator,0,CLSCTX_ALL,&IID_IMMDeviceEnumerator,(void**)&enumerator);
 if(FAILED(hr)){printf("ENUMERATOR_ERROR=%08lx\n",(unsigned long)hr);CoUninitialize();return 4;}
 hr=IMMDeviceEnumerator_EnumAudioEndpoints(enumerator,eRender,DEVICE_STATE_ACTIVE,&devices);
 if(SUCCEEDED(hr))hr=IMMDeviceCollection_GetCount(devices,&device_count);
 printf("READ_ONLY_SESSION_AUDIT target_pid=%lu devices=%u hr=%08lx\n",(unsigned long)wanted,device_count,(unsigned long)hr);
 for(UINT d=0;d<device_count;d++){
 IMMDevice *device=0;IAudioSessionManager2 *manager=0;IAudioSessionEnumerator *sessions=0;int count=0;
 hr=IMMDeviceCollection_Item(devices,d,&device);
 if(SUCCEEDED(hr))hr=IMMDevice_Activate(device,&IID_IAudioSessionManager2,CLSCTX_ALL,0,(void**)&manager);
 if(SUCCEEDED(hr))hr=IAudioSessionManager2_GetSessionEnumerator(manager,&sessions);
 if(SUCCEEDED(hr))hr=IAudioSessionEnumerator_GetCount(sessions,&count);
 for(int i=0;i<count;i++){
 IAudioSessionControl *control=0;IAudioSessionControl2 *control2=0;ISimpleAudioVolume *simple=0;IChannelAudioVolume *channels=0;DWORD pid=0;
 hr=IAudioSessionEnumerator_GetSession(sessions,i,&control);
 if(SUCCEEDED(hr))hr=IAudioSessionControl_QueryInterface(control,&IID_IAudioSessionControl2,(void**)&control2);
 if(SUCCEEDED(hr))hr=IAudioSessionControl2_GetProcessId(control2,&pid);
 if(SUCCEEDED(hr)&&pid==wanted){
 matches++;AudioSessionState state;hr=IAudioSessionControl_GetState(control,&state);
 printf("SESSION device=%u index=%d state=%d state_hr=%08lx\n",d,i,(int)state,(unsigned long)hr);
 hr=IAudioSessionControl_QueryInterface(control,&IID_ISimpleAudioVolume,(void**)&simple);
 if(SUCCEEDED(hr)){float v=-1;BOOL mute=FALSE;
 hr=ISimpleAudioVolume_GetMasterVolume(simple,&v);printf("MASTER value=%.9g hr=%08lx\n",(double)v,(unsigned long)hr);
 hr=ISimpleAudioVolume_GetMute(simple,&mute);printf("MUTE value=%d hr=%08lx\n",(int)mute,(unsigned long)hr);}
 hr=IAudioSessionControl_QueryInterface(control,&IID_IChannelAudioVolume,(void**)&channels);
 if(SUCCEEDED(hr)){UINT n=0;hr=IChannelAudioVolume_GetChannelCount(channels,&n);
 for(UINT c=0;SUCCEEDED(hr)&&c<n;c++){float v=-1;hr=IChannelAudioVolume_GetChannelVolume(channels,c,&v);printf("CHANNEL index=%u value=%.9g hr=%08lx\n",c,(double)v,(unsigned long)hr);}}
 }
 if(channels)IChannelAudioVolume_Release(channels);if(simple)ISimpleAudioVolume_Release(simple);
 if(control2)IAudioSessionControl2_Release(control2);if(control)IAudioSessionControl_Release(control);
 }
 if(sessions)IAudioSessionEnumerator_Release(sessions);if(manager)IAudioSessionManager2_Release(manager);if(device)IMMDevice_Release(device);
 }
 if(devices)IMMDeviceCollection_Release(devices);IMMDeviceEnumerator_Release(enumerator);CoUninitialize();
 printf("MATCHES=%u\n",matches);return matches?0:5;
}
