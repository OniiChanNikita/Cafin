import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

class MyApp(App):
    def build(self):
        self.headers = {'Authorization': 'Token 70ea8689002ad4a9ddd8efc32529e295137bf2b1'}
        # Основной макет приложения
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.canvas.before.clear()  # Очистить фон

        # Меню с кнопками "Показать" и "Создать"
        menu_layout = BoxLayout(orientation='horizontal', spacing=10)
        show_button = Button(text='Показать', on_press=self.show_list)
        create_button = Button(text='Создать', on_press=self.show_create_form)
        menu_layout.add_widget(show_button)
        menu_layout.add_widget(create_button)

        # Список элементов с автоматической полосой прокрутки
        self.item_list = BoxLayout(orientation='vertical', spacing=10)
        # self.item_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # self.item_list.bind(minimum_height=layout.setter("height"))
        self.scroll_view = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))

        self.scroll_view.add_widget(self.item_list)

        # Добавляем элементы на основной макет
        layout.add_widget(menu_layout)
        layout.add_widget(self.scroll_view)

        return layout

    def show_list(self, instance):
        url = 'http://176.53.162.130/'

        # Очистить список элементов и добавить несколько элементов для демонстрации
        elements = requests.get(url, headers=self.headers).json()
        print(elements)
        list_data = []
        for item in elements:
            list_data.append({'text': item['name']})
            label = Label(text='{'+'text: ' + item['name'] + '}')
            self.item_list.add_widget(label)

    def show_create_form(self, instance):
        # Показать поле для ввода и кнопку "Создать" только после нажатия кнопки "Создать"
        self.item_list.clear_widgets()
        self.input_field_submit = TextInput(hint_text='Введите текст', multiline=False)
        create_button = Button(text='Создать', on_press=self.submit_form)
        self.item_list.add_widget(self.input_field_submit)
        self.item_list.add_widget(create_button)

    def submit_form(self, instance):
        entered_text = self.input_field_submit.text
        url = 'http://127.0.0.1:8000/change_detail_profile_api/'
        post = requests.post(url, headers=self.headers, json={'name': entered_text})
        print("Текст, введенный в TextInput:", entered_text)

if __name__ == '__main__':
    MyApp().run()
