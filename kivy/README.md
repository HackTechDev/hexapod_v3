https://ressources.labomedia.org/kivy_buildozer#installation
https://wiki.labomedia.org/index.php/Kivy_Buildozer_pour_cr%C3%A9er_une_application_Android_avec_un_script_python.html#Compilation_d.27un_projet


buildozer.spec

android.accept_sdk_license = True
android.skip_update = False



sudo apt-get install aidl 

 util01@station40  ~/HEXAPOD/androidpy  cp /usr/bin/aidl ~/.buildozer/android/platform/android-sdk/build-tools/36.0.0-rc5 
 util01@station40  ~/HEXAPOD/androidpy  chmod +x ~/.buildozer/android/platform/android-sdk/build-tools/36.0.0-rc5/aidl 



util01@station40:~/.buildozer/android/platform/android-sdk/tools/bin$ ./sdkmanager --sdk_root=/home/util01/.buildozer/android/platform/android-sdk/  "platform-tools" "platforms;android-31"
Warning: Failed to find package build-tools:31.0.0                              
util01@station40:~/.buildozer/android/platform/android-sdk/tools/bin$ ./sdkmanager --sdk_root=/home/util01/.buildozer/android/platform/android-sdk/  "build-tools;31.0.0"

