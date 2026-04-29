import speech_recognition as sr

def listen_speech():
    r = sr.Recognizer()

    # 🔧 CHANGE INDEX IF NEEDED (try 1 first)
    mic = sr.Microphone(device_index=1)

    with mic as source:
        print("🎤 Speak now (max 5 seconds)...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected (timeout)")
            return ""

    try:
        text = r.recognize_google(audio)
        print("📝 You said:", text)
        return text

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""

    except sr.RequestError as e:
        print("❌ Speech service error:", e)
        return ""
