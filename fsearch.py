import socket
import webbrowser
import pyperclip
from googlesearch import search  # تأكد من استيراد مكتبة البحث
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.audio import SoundLoader  # لتحميل الصوت

# تغيير إعدادات نافذة Kivy لجعل الخلفية داكنة
Window.clearcolor = (0, 0, 0, 1)  # خلفية داكنة (أسود)

# تحميل الصوت عند الضغط على الأزرار
def play_sound(sound_file):
    sound = SoundLoader.load(sound_file)
    if sound:
        sound.play()

# التحقق من الاتصال بالإنترنت
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# البحث عن حسابات فيسبوك
def find_facebook_profiles(name, max_results=3):
    query = f"site:facebook.com {name}"
    try:
        return list(search(query, num_results=max_results, lang="ar"))
    except Exception as e:
        return [f"خطأ أثناء البحث: {e}"]

# نسخ إلى الحافظة
def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        play_sound('copy_sound.wav')  # إضافة صوت عند النسخ
        show_popup("تم النسخ", "تم نسخ الرابط إلى الحافظة.")
    except:
        play_sound('error_sound.wav')  # إضافة صوت عند حدوث خطأ
        show_popup("خطأ", "حدث خطأ أثناء النسخ.")

# عرض الرسائل المنبثقة
def show_popup(title, message):
    popup = Popup(title=title, content=Label(text=message, color=(0, 1, 0, 1), font_size=16),
                  size_hint=(0.6, 0.3), background_color=(0, 0, 0, 1))  # خلفية داكنة للنوافذ المنبثقة
    popup.open()

class FacebookSearchApp(App):
    def build(self):
        self.title = "أداة البحث عن حسابات فيسبوك"
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text="أدخل الاسم للبحث عن حسابات فيسبوك:", font_size=18, color=(0, 1, 0, 1)))

        self.input_name = TextInput(hint_text="أدخل اسم المستخدم", font_size=16, size_hint_y=None, height=40, multiline=False, 
                                    background_color=(0, 0, 0, 0.8), foreground_color=(0, 1, 0, 1))
        layout.add_widget(self.input_name)

        search_button = Button(text="بحث", font_size=18, background_normal='', background_color=(0, 1, 0, 0.6), size_hint_y=None, height=50)
        search_button.bind(on_press=self.search_profiles)
        layout.add_widget(search_button)

        self.result_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))

        scroll_view = ScrollView()
        scroll_view.add_widget(self.result_layout)

        layout.add_widget(scroll_view)

        return layout

    def search_profiles(self, instance):
        play_sound('click_sound.wav')  # إضافة صوت عند الضغط على زر البحث
        name = self.input_name.text.strip()
        if not name:
            play_sound('error_sound.wav')  # إضافة صوت عند حدوث خطأ
            show_popup("تنبيه", "يرجى إدخال اسم للبحث.")
            return

        if not check_internet():
            play_sound('error_sound.wav')  # إضافة صوت عند عدم الاتصال بالإنترنت
            show_popup("خطأ", "لا يوجد اتصال بالإنترنت.")
            return

        results = find_facebook_profiles(name)
        self.update_results(results)

    def update_results(self, results):
        self.result_layout.clear_widgets()

        if not results or "خطأ" in results[0]:
            self.result_layout.add_widget(Label(text=results[0], color=(1, 0, 0, 1), font_size=14, size_hint_y=None, height=40))
            return

        for url in results:
            result_button = Button(text=url, size_hint_y=None, height=40, background_normal='', background_color=(0, 0.5, 0, 0.4), 
                                   color=(0, 1, 0, 1))
            result_button.bind(on_press=lambda instance, u=url: webbrowser.open(u))
            self.result_layout.add_widget(result_button)

            copy_button = Button(text="نسخ", size_hint_y=None, height=40, background_normal='', background_color=(0, 0, 1, 0.5),
                                 color=(0, 1, 0, 1))
            copy_button.bind(on_press=lambda instance, u=url: copy_to_clipboard(u))
            self.result_layout.add_widget(copy_button)

if __name__ == "__main__":
    FacebookSearchApp().run()