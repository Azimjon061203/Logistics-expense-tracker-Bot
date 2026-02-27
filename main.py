from os import write
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import db, os
from dotenv import load_dotenv

user_language = {}
admin_language = {}

BOUND_GROUP_ID=-1003808900115
CARD={}
Admin_password = "120306"
Admin_ids = {357144029, 5559220292}

load_dotenv()
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN topilmadi!")

BAZA = {
    'start': {
        "uz": "Quyidagilardan birini tanlang 👇",
        "krl": "Қуйидагилардан бирини танланг 👇",
        "qzq": "Төмендегілердің бірін таңдаңыз 👇",
        "kg": "Төмөнкүдөрдүн бирин тандаңыз 👇",
        "ru": "Выберите один из следующих вариантов 👇",
        "eng": "Choose one of the following 👇",
    },
    "settings_language": {
        "uz": "Tilni tanlang: ",
        "krl": "Тилни танланг: ",
        "qzq": "Тілді таңдаңыз",
        "kg": "Тилди тандаңыз:",
        "ru": "Выберите язык: ",
        "eng": "Select language: ",
    }
}

start_user = {

    "uz": ["👤 Ism Familiyangizni kiriting: masalan:(Said Salimov) ", "☎️ Telefon raqamingizni yuboring! ",
           "Iltimos, telefon raqamingizni pastdagi tugma orqali yuboring 👇", "📍 Lokatsiyangizni yuboring: ",
           "Iltimos, lokatsiyangizni pastdagi tugma orqali yuboring 👇", "Mashinangizni rusumini tanlang 🚛",
           "Mashina kabinasi nomerlaridan birini tanlang 🚚", "🚚 Bu kategoryda mashina nomeri yoq ❗",
           "Mashina pritsepi nomerlaridan birini tanlang 🚚", "Yonalishingizni tanlang 🛣",
           "Ro'yxatdan o'tdingiz ✅", "Menyudagi tugmalardan birini tanlang 👇"],

    "krl": ["👤 Исм фамилиянгизни киритинг: масалан (Саид Салимов) ", "☎️ Телефон рақамингизни юборинг! ",
            "Илтимос, телефон рақамингизни пастдаги тугма орқали юборинг 👇", "📍 Локациянгизни юборинг: ",
            "Илтимос, локациянгизни пастдаги тугма орқали юборинг 👇", "Машинангиз русумини танланг 🚛",
            "Машина кабинаси номерларидан бирини танланг 🚚", "🚚 Бу категорияда машина номери йўқ ❗",
            "Машина прицепи номерларидан бирини танланг 🚚", "Йўналишингизни танланг 🛣",
            "Рўйхатдан ўтдингиз ✅", "Менюдаги тугмалардан бирини танланг 👇"],

    "qzq": ["👤 Атыңызды және тегіңызды енгізіңіз: мысалы (Said Salimov)", "☎️ Телефон нөміріңізді жіберіңіз!",
            "Өтінемін, телефон нөміріңізді төмендегі батырма арқылы жіберіңіз 👇", "📍 Орналасқан жеріңізді жіберіңіз: ",
            "Өтінемін, орналасқан жеріңізді төмендегі батырма арқылы жіберіңіз 👇", "Көлігіңіздің маркасын таңдаңыз 🚛",
            "Көлік кабинасының нөмірлерінің бірін таңдаңыз 🚚", "🚚 Бұл санатта көлік нөмірі жоқ ❗",
            "Көлік прицепінің нөмірлерінің бірін таңдаңыз 🚚", "Бағытыңызды таңдаңыз 🛣",
            "Тіркелдіңіз ✅", "Мәзірдегі түймелердің бірін таңдаңыз 👇"],

    "kg": ["👤 Атыңызды жана фамилияңызды киргизиңиз: мисалы (Said Salimov)", "☎️ Телефон номериңизди жөнөтүңүз!",
           "Сураныч, телефон номериңизди төмөнкү баскыч аркылуу жөнөтүңүз 👇", "📍 Локацияңызды жөнөтүңүз: ",
           "Сураныч, локацияңызды төмөнкү баскыч аркылуу жөнөтүңүз 👇", "Унааңыздын маркасын тандаңыз 🚛",
           "Унаа кабинасынын номерлеринин бирин тандаңыз 🚚", "🚚 Бул категорияда унаа номери жок ❗",
           "Унаа прицепинин номерлеринин бирин тандаңыз 🚚", "Жолуңузду тандаңыз 🛣",
           "Тизмеге катталдыңыз ✅", "Менюдагы баскычтардын бирин тандаңыз 👇"],

    "ru": ["👤 Введите имя и фамилию, например (Саид Салимов) ", "☎️ Отправьте ваш номер телефона! ",
           "Пожалуйста, отправьте свой номер телефона, нажав на кнопку ниже 👇", "📍 Отправьте вашу локацию: ",
           "Пожалуйста, отправьте свой локацию, нажав на кнопку ниже 👇", "Выберите марку вашего автомобиля 🚛",
           "Выберите один из номеров кабины автомобиля 🚚", "🚚 В этой категории нет номера машины ❗",
           "Прицепные номера автомобиля — выберите один из них 🚚", "Выберите направление 🛣",
           "Вы зарегистрировались ✅", "Выберите одну из кнопок меню 👇"],

    "eng": ["👤 Enter your first and last name, for example (Said Salimov) ", "☎️ Send your phone number! ",
            "Please send your phone number using the button below 👇", "📍 Send your location: ",
            "Please send your location using the button below 👇", "Choose your car model 🚛",
            "Choose one of the vehicle cabin numbers 🚚", "🚚 There is no vehicle number in this category ❗",
            "Choose one of the trailer numbers 🚚", "Choose your direction 🛣",
            "You have successfully registered ✅", "Choose one of the menu buttons 👇"],
}

MENU_BUTTONS = {

    "uz": ["📞 Raqam yuborish", "📍 Lokatsiya yuborish", "Toshkent -> Moskva", "Toshkent -> Sankt-Peterburg",
           "Toshkent -> Orenburg", "Toshkent -> Vladimir", "Moskva -> Toshkent", "San-Peterburg -> Toshkent",
           "Vladimir -> Toshkent", "Orenburg -> Toshkent", "💵 Kunlik harajatlar", "🛢 Yoqilg'i harajatlari",
           "🛠 Texnik harajatlar", "👮‍♂️ Transportni taroz rasxod", "🛣 Yo'nalish qo'shish", "Hisobotni topshirish 📑", "⚙️ Sozlamalar" ],

    "krl": ["📞 Рақам юбориш", "📍 Локация юбориш", "Тошкент -> Москва", "Тошкент -> Санкт-Петербург",
            "Тошкент -> Оренбург", "Тошкент -> Владимир", "Москва -> Тошкент", "Санкт-Петербург -> Тошкент",
            "Владимир -> Тошкент", "Оренбург -> Тошкент", "💵 Кунлик харажатлар", "🛢 Ёқилғи харажатлари",
            "🛠 Техник харажатлар", "👮‍♂️ Транспортни тарози харажати", "🛣 Йўналиш қўшиш", "Ҳисоботни топшириш 📑", "⚙️ Созламалар"],

    "qzq": ["📞 Нөмірді жіберу", "📍 Орналасқан жерді жіберу", "Ташкент -> Мәскеу", "Ташкент -> Санкт-Петербург",
            "Ташкент -> Орынбург", "Ташкент -> Владимир", "Мәскеу -> Ташкент", "Санкт-Петербург -> Ташкент",
            "Владимир -> Ташкент", "Орынбург -> Ташкент", "💵 Күнделікті шығындар", "🛢 Жанармай шығындары",
            "🛠 Техникалық шығындар", "👮‍♂️ Көлік таразы шығыны", "🛣 Бағыт қосу", "Есепті тапсыру 📑", "⚙️ Baptaýlar"],

    "kg": ["📞 Номерди жөнөтүү", "📍 Локацияны жөнөтүү", "Ташкент -> Москва", "Ташкент -> Санкт-Петербург",
           "Ташкент -> Оренбург", "Ташкент -> Владимир", "Москва -> Ташкент", "Санкт-Петербург -> Ташкент",
           "Владимир -> Ташкент", "Оренбург -> Ташкент", "💵 Күнүмдүк чыгымдар", "🛢 Күйүүчү май чыгымдары",
           "🛠 Техникалык чыгымдар", "👮‍♂️ Транспорт тараза чыгымы", "🛣 Багыт кошуу", "Баяндама тапшыруу 📑", "⚙️ Орнотуулар"],

    "ru": ["📞 Отправить номер", "📍 Отправить локацию","Ташкент -> Москва", "Ташкент -> Санкт-Петербург",
           "Ташкент -> Оренбург", "Ташкент -> Владимир", "Москва -> Тошкент", "Санкт-Петербург -> Тошкент",
           "Владимир -> Тошкент", "Оренбург -> Тошкент", "💵 Ежедневные расходы", "🛢 Расходы на топливо",
           "🛠 Технические расходы", "👮‍♂️ Расходы на взвешивание транспорта", "🛣 Добавить маршрут", "Сдать отчёт 📑", "⚙️ Настройки"],

    "eng": ["📞 Send number", "📍 Send location", "Tashkent -> Moscow", "Tashkent -> Saint Petersburg",
            "Tashkent -> Orenburg", "Tashkent -> Vladimir", "Moscow -> Tashkent", "Saint Petersburg -> Tashkent",
            "Vladimir -> Tashkent", "Orenburg -> Tashkent", "💵 Daily expenses", "🛢 Fuel expenses",
            "🛠 Technical expenses", "👮‍♂️ Transport scale expense", "🛣 Add route", "Submit the report 📑", "⚙️ Settings"],

}
YANGI_YONALISH={
    "uz" : ["Orenburg -> Sterlitamak", "Samara -> Ufa", "Samara -> Kazan", "Ufa -> Kazan", "Penza -> Moskva", "Moskva -> Sanpeterburg",
            "Penza -> Sanpeterburg", "Chelyabnskiy -> Ekaterinburg", "Ekaterinburg -> Perm", "Chelyabnskiy -> Perm", "Barnaul -> Nozosibirisk",
            "Novosibirsk -> Tomsk", "Tomsk -> Krasnayarsk", "Krasnayarsk -> Irkutisk", "Tomsk -> Irkutskiy", "Barnaul -> Tomsk"],

    "krl" : ["Оренбург → Стерлитамак", "Самара → Уфа", "Самара → Қaзaн", "Уфа → Қазан", "Пенза → Москва", "Москва → Санкт-Петербург",
             "Пенза → Санкт-Петербург","Челябинск → Екатеринбург", "Екатеринбург → Перм", "Челябинск → Перм", "Барнаул → Новосибирск",
             "Новосибирск → Томск", "Томск → Красноярск", "Красноярск → Иркутск", "Томск → Иркутск", "Барнаул → Томск"],

    "qzq" : ["Орынбор → Стерлитамақ", "Самара → Уфа", "Самара → Қазан", "Уфа → Қазан", "Пенза → Мәскеу", "Мәскеу → Санкт-Петербург",
             "Пенза → Санкт-Петербург", "Челябі → Екатеринбург", "Екатеринбург → Пермь", "Челябі → Пермь", "Барнаул → Новосібір",
             "Новосібір → Томск", "Томск → Красноярск", "Красноярск → Иркутск", "Томск → Иркутск", "Барнаул → Томск"],

    "kg" : ["Оренбург → Стерлитамак", "Самара → Уфа", "Самара → Казань", "Уфа → Казань", "Пенза → Москва", "Москва → Санкт-Петербург",
            "Пенза → Санкт-Петербург", "Челябинск → Екатеринбург", "Екатеринбург → Пермь", "Челябинск → Пермь", "Барнаул → Новосибирск",
            "Новосибирск → Томск", "Томск → Красноярск", "Красноярск → Иркутск", "Томск → Иркутск", "Барнаул → Томск"],

    "ru" : ["Оренбург → Стерлитамак", "Самара → Уфа", "Самара → Казань", "Уфа → Казань", "Пенза → Москва", "Москва → Санкт-Петербург",
            "Пенза → Санкт-Петербург", "Челябинск → Екатеринбург", "Екатеринбург → Пермь", "Челябинск → Пермь", "Барнаул → Новосибирск",
            "Новосибирск → Томск", "Томск → Красноярск", "Красноярск → Иркутск", "Томск → Иркутск", "Барнаул → Томск"],

    "eng" : ["Orenburg → Sterlitamak", "Samara → Ufa", "Samara → Kazan", "Ufa → Kazan", "Penza → Moscow", "Moscow → Saint Petersburg",
             "Penza → Saint Petersburg", "Chelyabinsk → Yekaterinburg", "Yekaterinburg → Perm", "Chelyabinsk → Perm", "Barnaul → Novosibirsk",
             "Novosibirsk → Tomsk", "Tomsk → Krasnoyarsk", "Krasnoyarsk → Irkutsk", "Tomsk → Irkutsk", "Barnaul → Tomsk"],
}

MENU_TRANSPORTNI_JOYLASHUVI={
    "uz" : ["Chimkent", "Turkiston", "Qizilo'rda", "Jayson", "Arkbuloq", "Arenburg", "Makshan", "Ryazan", "Mikad", "Voskresemni", "Kolumna"],
    "krl" : ["Чимкент", "Туркистон", "Қизилўрда", "Жэйсон", "Аркбулоқ", "Аренбург", "Макшан", "Рязан", "Микад", "Воскресемни", "Колумна"],
    "qzq" : ["Шымкент", "Түркістан", "Қызылорда", "Жэйсон", "Аркбұлақ", "Аренбург", "Макшан", "Рязань", "Микад", "Воскресемни", "Колумна"],
    "kg" : ["Чимкент", "Түркстан", "Кызыл-Орда", "Жэйсон", "Аркбулак", "Аренбург", "Макшан", "Рязань", "Микад", "Воскресемни", "Колумна"],
    "ru" : ["Чимкент", "Туркестан", "Кызылорда", "Джейсон", "Аркбулок", "Аренбург", "Макшан", "Рязань", "Микад", "Воскресемни", "Колонна"],
    "eng" : ["Chimkent", "Turkistan", "Kyzylorda", "Jayson", "Arkbuloq", "Arenburg", "Makshan", "Ryazan", "Mikad", "Voskresemni", "Kolumna"],
}


USER_MENU_BUYRUQLAR={

    "uz" : ["💵 Pul valuyatasini tanlang:","Quyidagilardan birini tanglang 👇", "💵 Oziq - ovqat uchun ketgan pul miqdorini kiriting:",
            "🅿️ Stayanka uchun ketgan pul miqdorini kiriting:", "📞 Telefonni oylik to'lovi uchun ketgan pul miqdorinin kiriting:",
            "1l yoqilg'i narxini yozing ✍️", "Umumiy yoqilgi hajmini yozing ✍️ -> masalan 👉10", "🛞 Balon uchun ketgan pul miqdorini kiriting:",
            "🚛 Mashina motori uchun ketgan pul miqdorini kiriting:", "🛢 Mashina yog'i uchun ketgan pul miqdorini kiriting:",
            "🛢 Mashina antfrisi uchun ketgan pul miqdorini kiriting:", "🛢 Mashina aftoli uchun ketgan pul miqdorini kiriting:",
            "✅ Stayanka harajati saqlandi", "✅ Telefon harajati saqlandi", "🛢 Yoqilg‘i harajati saqlandi ✅", "Ma’lumotlaringiz saqlandi ✅",
            "oziq ovqat xarajatlari saqlandi ✅", "Balon xarajatlari saqlandi ✅", "Motor xarajatlari saqlandi ✅", "Antfris xarajatlari saqlandi ✅",
            "Aftol xarajatlari saqlandi ✅", "Til o‘zgartirildi ✅", "🚛 Transportni taroziga ketgan pul miqdorini kiriting:",
            "Taransportni xarajatlar saqlandi ✅", "Yangi yo'nalish saqlandi ✅ ", "Yangi lokatsiya saqlandi ✅", "Oziq-ovqat harajatlari saqlandi ✅"],

    "krl" : ["💵 Пул валютасини танланг:", "Қуйидагилардан бирини танланг 👇", "💵 Озиқ-овқат учун кетган пул миқдорини киритинг:",
             "🅿️ Стоянка учун кетган пул миқдорини киритинг:", "📞 Телефоннинг ойлик тўлови учун кетган пул миқдорини киритинг:",
             "1 л ёқилғи нархини ёзинг ✍️", "Умумий ёқилғи xажмини ёзинг ✍️ → масалан 👉 10","🛞 Балон учун кетган пул миқдорини киритинг:",
             "🚛 Машина мотори учун кетган пул миқдорини киритинг: ","🛢 Машина ёғи учун кетган пул миқдорини киритинг:",
             "🛢 Машина антифризи учун кетган пул миқдорини киритинг:", "🛢 Машина афтоли учун кетган пул миқдорини киритинг:",
             "✅ Стаянка харажати сақланди", "✅ Телефон харажати сақланди", "🛢 Ёқилғи харажати сақланди ✅", "Маълумотларингиз сақланди ✅",
             "Озиқ-овқат харажатлари сақланди ✅", "Балон харажатлари сақланди ✅", "Мотор харажатлари сақланди ✅", "Антифриз харажатлари сақланди ✅",
             "Афтол харажатлари сақланди ✅", "Тил ўзгартирилди ✅", "🚛 Транспортни тарозига кетган пул миқдорини киритинг:",
             "Транспорт харажатлари сақланди ✅", "Янги йўналиш сақланди ✅", "Янги локация сақланди ✅", "Озиқ-овқат харажатлари сақланди ✅"],

    "qzq" : ["💵 Валютаны таңдаңыз:", "Төмендегілердің бірін таңдаңыз 👇", "💵 Азық-түлікке кеткен ақша мөлшерін енгізіңіз:",
             "🅿️ Тұраққа кеткен ақша мөлшерін енгізіңіз:", "📞 Телефонның айлық төлеміне кеткен ақша мөлшерін енгізіңіз:",
             "1 л жанармай бағасын жазыңыз ✍️" , "Жалпы жанармай көлемін жазыңыз ✍️ → мысалы 👉 10","🛞 Дөңгелекке кеткен ақша мөлшерін енгізіңіз:",
             "🚛 Көлік қозғалтқышына кеткен ақша мөлшерін енгізіңіз:","🛢 Көлік майына кеткен ақша мөлшерін енгізіңіз:",
             "🛢 Көлік антифризіне кеткен ақша мөлшерін енгізіңіз:", "🛢 Көлік жанармайына кеткен ақша мөлшерін енгізіңіз:",
             "✅ Тұрақ шығыны сақталды", "✅ Телефон шығыны сақталды", "🛢 Жанармай шығыны сақталды ✅", "Деректеріңіз сақталды ✅",
             "Азық-түлік шығындары сақталды ✅", "Дөңгелек шығындары сақталды ✅", "Қозғалтқыш шығындары сақталды ✅", "Антифриз шығындары сақталды ✅",
             "Жанармай шығындары сақталды ✅", "Тіл өзгертілді ✅", "🚛 Көлікті таразыға тартуға кеткен ақша мөлшерін енгізіңіз:",
             "Көлік шығындары сақталды ✅", "Жаңа бағыт сақталды ✅", "Жаңа локация сақталды ✅", "Азық-түлік шығындары сақталды ✅"],

    "kg" : ["💵 Валютаны тандаңыз:", "Төмөнкүлөрдүн бирин тандаңыз 👇", "💵 Азык-түлүккө кеткен акчанын суммасын киргизиңиз:",
            "🅿️ Токтотмо үчүн кеткен акчанын суммасын киргизиңиз:", "📞 Телефондун айлык төлөмү үчүн кеткен акчанын суммасын киргизиңиз:",
            "1 л күйүүчү майдын баасын жазыңыз ✍️", "Жалпы күйүүчү май көлөмүн жазыңыз ✍️ → мисалы 👉 (10)","🛞 Дөңгөлөк үчүн кеткен акчанын суммасын киргизиңиз:",
            "🚛 Унаанын кыймылдаткычы үчүн кеткен акчанын суммасын киргизиңиз:", "🛢 Унаа майы үчүн кеткен акчанын суммасын киргизиңиз:",
            "🛢 Унаа антифризи үчүн кеткен акчанын суммасын киргизиңиз:", "🛢 Унаа күйүүчү майы үчүн кеткен акчанын суммасын киргизиңиз:",
            "✅ Токтотмо чыгымы сакталды", "✅ Телефон чыгымы сакталды", "🛢 Күйүүчү май чыгымы сакталды ✅", "Маалыматтарыңыз сакталды ✅",
            "Азык-түлүк чыгымдары сакталды ✅", "Дөңгөлөк чыгымдары сакталды ✅", "Кыймылдаткыч чыгымдары сакталды ✅", "Антифриз чыгымдары сакталды ✅",
            "Күйүүчү май чыгымдары сакталды ✅", "Тіл өзгертілді ✅", "🚛 Транспортту таразага тартууга кеткен акча суммасын киргизиңиз:",
            "Транспорт чыгымдары сакталды ✅", "Жаңы багыт сакталды ✅", "Жаңы локация сакталды ✅", "Азык-түлүк чыгымдары сакталды ✅"],

    "ru" : ["💵 Выберите валюту:", "Выберите один из следующих вариантов 👇", "💵 Введите сумму расходов на продукты:",
            "🅿️ Введите сумму расходов на парковку:", "📞 Введите сумму ежемесячной оплаты телефона:",
            "Введите цену 1 л топлива ✍️", "Введите общий объём топлива ✍️ → например 👉 10","🛞 Введите сумму расходов на шины:",
            "🚛 Введите сумму расходов на двигатель автомобиля:", "🛢 Введите сумму расходов на моторное масло:",
            "🛢 Введите сумму расходов на антифриз:","🛢 Введите сумму расходов на топливо:",
            "✅ Расход за стоянку сохранён", "✅ Расходы на телефон сохранены", "🛢 Расходы на топливо сохранены ✅", "Ваши данные сохранены ✅",
            "Расходы на продукты сохранены ✅","Расходы на шины сохранены ✅", "Расходы на двигатель сохранены ✅", "Расходы на антифриз сохранены ✅",
            "Расходы на топливо сохранены ✅", "Язык изменён ✅", "🚛 Введите сумму, потраченную на взвешивание транспорта:",
            "Расходы на транспорт сохранены ✅", "Новый маршрут сохранён ✅", "Новая локация сохранена ✅", "Расходы на питание сохранены ✅"],

    "eng" : ["💵 Select currency:", "Choose one of the following 👇", "💵 Enter food expenses amount:",
             "🅿️ Enter the amount of money spent on parking:", "📞 Enter monthly phone payment amount:",
             "Enter the price of 1 liter of fuel ✍️", "Enter the total fuel volume ✍️ → for example 👉 (10)", "🛞 Enter the amount of money spent on tires:",
             "🚛 Enter vehicle engine expenses amount:", "🛢 Enter engine oil expenses amount:",
             "🛢 Enter antifreeze expenses amount:","🛢 Enter fuel expenses amount:",
             "✅ Parking expense saved", "✅ Phone expense saved", "🛢 Fuel expense has been saved ✅", "Your information has been saved ✅",
             "Food expenses saved ✅", "Tire expenses saved ✅", "Engine expenses saved ✅", "Antifreeze expenses saved ✅",
             "Fuel expenses saved ✅", "Language changed ✅", "🚛 Enter the amount spent on vehicle weighing:",
             "Transport expenses have been saved ✅", "New route saved ✅", "New location saved ✅", "Food expenses saved ✅"]
}


CHEK_BUYRUQLAR = {

    "uz": [
        "oziq-ovqat chekini yuboring 🧾:", "stayanka chekini yuboring 🧾:", "telefon chekini yuboring 🧾:", "yoqilgi chekini yuboring 🧾:",
        "balon chekini yuboring 🧾:", "antfris chekini yuboring 🧾:", "aftol chekini yuboring 🧾:",
        "Iltimos, oziq-ovqat chekingizni rasm shaklida yuboring 📸", "Iltimos, stayanka chekini rasm shaklida yuboring 📸",
        "Iltimos, telefon chekini rasm shaklida yuboring 📸", "Iltimos, yoqilg'i chekini rasm shaklida yuboring 📸",
        "Iltimos, balon chekingizni rasm shaklida yuboring 📸",
        "Iltimos, antfris chekingizni rasm shaklida yuboring 📸", "Iltimos, aftol chekingizni rasm shaklida yuboring 📸"
    ],

    "krl": [
        "Озиқ-овқат чекини юборинг 🧾:", "Стаянка чекини юборинг 🧾:", "Телефон чекини юборинг 🧾:", "Ёқилғи чекини юборинг 🧾:",
        "Балон чекини юборинг 🧾:", "Антифриз чекини юборинг 🧾:", "Автол чекини юборинг 🧾:",
        "Илтимос, озиқ-овқат чекини расм шаклида юборинг 📸", "Илтимос, стаянка чекини расм шаклида юборинг 📸",
        "Илтимос, телефон чекини расм шаклида юборинг 📸", "Илтимос, ёқилғи чекини расм шаклида юборинг 📸",
        "Илтимос, балон чекини расм шаклида юборинг 📸",
        "Илтимос, антифриз чекини расм шаклида юборинг 📸", "Илтимос, автол чекини расм шаклида юборинг 📸"
    ],

    "qzq": [
        "Азық-түлік чегін жіберіңіз 🧾:", "Тұрақ чегін жіберіңіз 🧾:", "Телефон чегін жіберіңіз 🧾:", "Жанармай чегін жіберіңіз 🧾:",
        "Баллон чегін жіберіңіз 🧾:", "Антифриз чегін жіберіңіз 🧾:", "Автол чегін жіберіңіз 🧾:",
        "Өтінемін, азық-түлік түбіртегін фото түрінде жіберіңіз 📸", "Өтінемін, тұрақ түбіртегін фото түрінде жіберіңіз 📸",
        "Өтінемін, телефон түбіртегін фото түрінде жіберіңіз 📸", "Өтінемін, жанармай түбіртегін фото түрінде жіберіңіз 📸",
        "Өтінемін, баллон түбіртегін фото түрінде жіберіңіз 📸",
        "Өтінемін, антифриз түбіртегін фото түрінде жіберіңіз 📸", "Өтінемін, автол түбіртегін фото түрінде жіберіңіз 📸"
    ],

    "kg": [
        "Азык-түлүк чегин жибериңиз 🧾:", "Токтотмо жайдын чегин жибериңиз 🧾:", "Телефон чегин жибериңиз 🧾:", "Күйүүчү май чегин жибериңиз 🧾:",
        "Баллон чегин жибериңиз 🧾:", "Антифриз чегин жибериңиз 🧾:", "Автол чегин жибериңиз 🧾:",
        "Сураныч, азык-түлүк чегин сүрөт түрүндө жибериңиз 📸", "Сураныч, токтотмо жайдын чегин сүрөт түрүндө жибериңиз 📸",
        "Сураныч, телефон чегин сүрөт түрүндө жибериңиз 📸", "Сураныч, күйүүчү май чегин сүрөт түрүндө жибериңиз 📸",
        "Сураныч, баллон чегин сүрөт түрүндө жибериңиз 📸",
        "Сураныч, антифриз чегин сүрөт түрүндө жибериңиз 📸", "Сураныч, автол чегин сүрөт түрүндө жибериңиз 📸"
    ],

    "ru": [
        "Отправьте чек за продукты 🧾:", "Отправьте чек за стоянку 🧾:", "Отправьте чек за телефон 🧾:", "Отправьте чек за топливо 🧾:",
        "Отправьте чек за баллон 🧾:", "Отправьте чек за антифриз 🧾:", "Отправьте чек за автол 🧾:",
        "Пожалуйста, отправьте чек за продукты в виде фотографии 📸", "Пожалуйста, отправьте чек за стоянку в виде фотографии 📸",
        "Пожалуйста, отправьте чек за телефон в виде фотографии 📸", "Пожалуйста, отправьте чек за топливо в виде фотографии 📸",
        "Пожалуйста, отправьте чек за баллон в виде фотографии 📸",
        "Пожалуйста, отправьте чек за антифриз в виде фотографии 📸", "Пожалуйста, отправьте чек за автол в виде фотографии 📸"
    ],

    "eng": [
        "Please send the food receipt 🧾:", "Please send the parking receipt 🧾:", "Please send the phone receipt 🧾:", "Please send the fuel receipt 🧾:",
        "Please send the gas cylinder receipt 🧾:", "Please send the antifreeze receipt 🧾:", "Please send the motor oil receipt 🧾:",
        "Please send the food receipt as a photo 📸", "Please send the parking receipt as a photo 📸",
        "Please send the phone receipt as a photo 📸", "Please send the fuel receipt as a photo 📸",
        "Please send the gas cylinder receipt as a photo 📸",
        "Please send the antifreeze receipt as a photo 📸", "Please send the motor oil receipt as a photo 📸"
    ]
}

USER_MENU_ICHKI_BUTTONS={
    "uz" : ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🍲 Oziq - ovqat", "🅿️ Stayanka","📱 Telefon", "🛞 Balon", "🚛 Motor", "🛢 Yog'lar", "🛢 Antfris",
            "🛢 Aftol", "⬅️ Orqaga", "🇺🇿 Tilni o'zgartirish", "Saqlash ✅", "📍 Lokatsiya jo'natish", "📍 Lokatsiya yuborish"],

    "krl" : ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🍲 Озиқ-овқат", "🅿️ Стоянка","📱 Телефон", "🛞 Балон", "🚛 Мотор",  "🛢 Ёғлар", "🛢 Антифриз",
             "🛢 Афтол", "⬅️ Орқага", "🇺🇿 Тилни ўзгартириш", "Сақлаш ✅", "📍 Локация жўнатиш", "📍 Локация юбориш"],

    "qzq" : ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🍲 Азық-түлік", "🅿️ Тұрақ", "📱 Телефон", "🛞 Дөңгелек", "🚛 Қозғалтқыш", "🛢 Майлар", "🛢 Антифриз",
             "🛢 Жанармай", "⬅️ Артқа", "🇵🇼 Тілді өзгерту", "Сақтау ✅", "📍 Орналасқан жерді жіберу", "📍 Орналасқан жерді жіберу"],

    "kg" : ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🍲 Азык-түлүк", "🅿️ Токтотмо", "📱 Телефон", "🛞 Дөңгөлөк", "🚛 Кыймылдаткыч", "🛢 Майлар", "🛢 Антифриз",
            "🛢 Күйүүчү май", "⬅️ Артка", "🇰🇬 Тилди өзгөртүү", "Сактоо ✅", "📍 Жайгашкан жерди жөнөтүү", "📍 Жайгашкан жерди жөнөтүү"],

    "ru" : ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🍲 Продукты питания", "🅿️ Стоянка", "📱 Телефон", "🛞 Шина", "🚛 Двигатель", "🛢 Масла", "🛢 Антифриз",
            "🛢 Топливо", "⬅️ Назад", "🇷🇺 Изменить язык", "Сохранить ✅", "📍 Отправить локацию", "📍 Отправить локацию"],

    "eng" : ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🍲 Food", "🅿️ Parking", "📱 Phone", "🛞 Tire", "🚛 Engine", "🛢 Oils", "🛢 Antifreeze",
             "🛢 Antifreeze", "⬅️ Back", "🇺🇸 Change language", "Save ✅", "📍 Send location", "📍 Send location"],
}


ADMIN_USER = {
    "uz": [
        "Admin paneliga kirish uchun /admin <parol> yozing ❗",
        "❗ Foydalanish: /admin 1234",
        "❌ Parol noto'g'ri!",
        "🔐 Admin paneliga xush kelibsiz!",
        "🚚 Yuk mashinasi rusumini kiriting: masalan (DAF)",
        "Yuk mashinasi nomi qo'shildi ✅",
        "Mashina nomlaridan birini tanlang 👇",
        "Kabina nomeri qaysi davlatga tegishli ekanini tanlang 👇",
        "❌ Yuk mashinasi nomi topilmadi, qayta tanlang:",
        "Kabina nomerini 👉 01| A 111 BB ko'rinishda yozing ❗",
        "Mashina kabinasi nomeri muvaffaqiyatli qo'shildi ✅",
        "Iltimos, to‘g‘ri ma’lumot kiriting ❗",
        "Pritsep nomeri qaysi davlatga tegishli ekanini tanlang 👇",
        "Pritsep nomerini 👉 01| A 1010 CC yoki 01| A 111 BB ko'rinishda yozing ❗",
        "Pritsep nomeri muvaffaqiyatli qo'shildi ✅"
    ],

    "krl": [
        "Админ панелига кириш учун /admin <парол> ёзинг ❗",
        "❗ Фойдаланиш: /admin 1234",
        "❌ Парол нотўғри!",
        "🔐 Админ панелига хуш келибсиз!",
        "🚚 Юк машинаси русумини киритинг: масалан (DAF)",
        "Юк машинаси номи қўшилди ✅",
        "Машина номларидан бирини танланг 👇",
        "Кабина номери қайси давлатга тегишлилигини танланг 👇",
        "❌ Юк машинаси номи топилмади, қайта танланг:",
        "Кабина номерини 👉 01| A 111 BB кўринишда ёзинг ❗",
        "Машина кабинаси номери муваффақиятли қўшилди ✅",
        "Илтимос, тўғри маълумот киритинг ❗",
        "Притсеп номери қайси давлатга тегишлилигини танланг 👇",
        "Притсеп номерини 👉 01| A 1010 CC ёки 01| A 111 BB кўринишда ёзинг ❗",
        "Притсеп номери муваффақиятли қўшилди ✅"
    ],

    "qzq": [
        "Әкімші панеліне кіру үшін /admin <құпиясөз> жазыңыз ❗",
        "❗ Қолдану: /admin 1234",
        "❌ Құпия сөз қате!",
        "🔐 Админ панеліне қош келдіңіз!",
        "🚚 Жүк көлігінің маркасын енгізіңіз: мысалы (DAF)",
        "Жүк көлігінің атауы қосылды ✅",
        "Жүк көлігінің бірін таңдаңыз 👇",
        "Кабина нөмірі қай елге тиесілі екенін таңдаңыз 👇",
        "❌ Жүк көлігінің атауы табылмады, қайта таңдаңыз:",
        "Кабина нөмірін 👉 01| A 111 BB түрінде жазыңыз ❗",
        "Машина кабинасының нөмірі сәтті қосылды ✅",
        "Өтінемін, дұрыс мәлімет енгізіңіз ❗",
        "Притцеп нөмірі қай елге тиесілі екенін таңдаңыз 👇",
        "Притцеп нөмірін 👉 01| A 1010 CC немесе 01| A 111 BB түрінде жазыңыз ❗",
        "Притцеп нөмірі сәтті қосылды ✅"
    ],

    "kg": [
        "Админ панелине кирүү үчүн /admin <сырсөз> жазыңыз ❗",
        "❗ Колдонуу: /admin 1234",
        "❌ Сырсөз туура эмес!",
        "🔐 Админ панелге кош келиңиз!",
        "🚚 Жүк унаасынын маркасын киргизиңиз: мисалы (DAF)",
        "Жүк унаасынын аты кошулду ✅",
        "Жүк унаасынын бирин тандаңыз 👇",
        "Кабина номери кайсы өлкөгө таандык экенин тандаңыз 👇",
        "❌ Жүк унаасынын аты табылган жок, кайра тандаңыз:",
        "Кабина номерин 👉 01| A 111 BB форматында жазыңыз ❗",
        "Машина кабинасынын номери ийгиликтүү кошулду ✅",
        "Сураныч, туура маалыматты киргизиңиз ❗",
        "Притцеп номери кайсы өлкөгө таандык экенин тандаңыз 👇",
        "Притцеп номерин 👉 01| A 1010 CC же 01| A 111 BB форматында жазыңыз ❗",
        "Притцеп номери ийгиликтүү кошулду ✅"
    ],

    "ru": [
        "Для входа в админ-панель введите /admin <пароль> ❗",
        "❗ Использование: /admin 1234",
        "❌ Пароль неверный!",
        "🔐 Добро пожаловать в панель администратора!",
        "🚚 Введите марку грузовика, например (DAF)",
        "Название грузовика добавлено ✅",
        "Выберите грузовик 👇",
        "Выберите страну, которой принадлежит номер кабины 👇",
        "❌ Название грузовика не найдено, выберите снова:",
        "Введите номер кабины в формате 👉 01| A 111 BB ❗",
        "Номер кабины успешно добавлен ✅",
        "Пожалуйста, введите корректные данные ❗",
        "Выберите страну, которой принадлежит номер прицепа 👇",
        "Введите номер прицепа в формате 👉 01| A 1010 CC или 01| A 111 BB ❗",
        "Номер прицепа успешно добавлен ✅"
    ],

    "eng": [
        "To access the admin panel, enter /admin <password> ❗",
        "❗ Usage: /admin 1234",
        "❌ Incorrect password!",
        "🔐 Welcome to the admin panel!",
        "🚚 Enter the truck model, e.g. (DAF)",
        "Truck name added ✅",
        "Choose a truck model 👇",
        "Select the country the cabin number belongs to 👇",
        "❌ Truck model not found, please choose again:",
        "Enter the cabin number in the format 👉 01| A 111 BB ❗",
        "Cabin number successfully added ✅",
        "Please enter the correct information ❗",
        "Select the country the trailer number belongs to 👇",
        "Enter the trailer number in the format 👉 01| A 1010 CC or 01| A 111 BB ❗",
        "Trailer number successfully added ✅"
    ]
}

ADMIN_BUTTONS = {
    "uz": ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🚛 Yuk mashina nomini qo'shish", "🚚 Mashina kabinasi nomerini qo'shish",
           "🚚 Pritsep nomerini qo'shish", "⬅️ Orqaga"],

    "krl": ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🚛 Юк машина номи қўшиш", "🚚 Машина кабинаси номери қўшиш",
            "🚚 Притсеп номери қўшиш", "⬅️ Орқага"],

    "qzq": ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🚛 Жүк көлігінің атауын қосу", "🚚 Машина кабинасының нөмірін қосу",
            "🚚 Притцеп нөмірін қосу", "⬅️ Артқа"],

    "kg": ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🚛 Жүк унаасынын атын кошуу", "🚚 Машина кабинасынын номерин кошуу",
           "🚚 Притцеп номерин кошуу", "⬅️ Артка"],

    "ru": ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🚛 Добавить название грузовика", "🚚 Добавить номер кабины",
           "🚚 Добавить номер прицепа", "⬅️ Назад"],

    "eng": ["🇺🇿", "🇵🇼", "🇰🇬", "🇷🇺", "🇺🇸", "🚛 Add truck name", "🚚 Add cabin number",
            "🚚 Add trailer number", "⬅️ Back"]
}

LANGUAGE_BUTTON = {
    "uz": [("🇺🇿 O'zbekcha", 'lang_uz'), ("🇺🇿 Krilcha", 'lang_krl'), ("🇵🇼 Qozoqcha", 'lang_qzq'),
           ("🇰🇬 Qirg'izcha", "lang_kg"), ("🇷🇺 Russkiy", 'lang_ru'), ("🇬🇧 English", 'lang_eng')],

    "krl": [("🇺🇿 Ўзбекча", 'lang_uz'), ("🇺🇿 Кириллча", 'lang_krl'), ("🇰🇿 Қозоқча", 'lang_qzq'),
            ("🇰🇬 Қирғизча", "lang_kg"), ("🇷🇺 Русча", 'lang_ru'), ("🇬🇧 Инглизча", 'lang_eng')],

    "qzq": [("🇺🇿 Өзбекше", 'lang_uz'), ("🇺🇿 Кириллше", 'lang_krl'), ("🇰🇿 Қазақша", 'lang_qzq'),
            ("🇰🇬 Қырғызша", "lang_kg"), ("🇷🇺 Орысша", 'lang_ru'), ("🇬🇧 Ағылшынша", 'lang_eng')],

    "kg": [("🇺🇿 Өзбекче", 'lang_uz'), ("🇺🇿 Кириллче", 'lang_krl'), ("🇰🇿 Казакча", 'lang_qzq'),
           ("🇰🇬 Кыргызча", "lang_kg"), ("🇷🇺 Орусча", 'lang_ru'), ("🇬🇧 Англисче", 'lang_eng')],

    "ru": [("🇺🇿 Узбекский", 'lang_uz'), ("🇺🇿 Кириллический", 'lang_krl'), ("🇰🇿 Казахский", 'lang_qzq'),
           ("🇰🇬 Киргизский", "lang_kg"), ("🇷🇺 Русский", 'lang_ru'), ("🇬🇧 Английский", 'lang_eng')],

    "eng": [("🇺🇿 Uzbek", 'lang_uz'), ("🇺🇿 Cyrillic", 'lang_krl'), ("🇰🇿 Kazakh", 'lang_qzq'),
            ("🇰🇬 Kyrgyz", "lang_kg"), ("🇷🇺 Russian", 'lang_ru'), ("🇬🇧 English", 'lang_eng')]
}

USER_LANGUAGE = {
    "uz": ["Botni boshlash uchun /start ni bosing", "️ Oldingi joydan davom etyapmiz. Davom eting 👇"],
    "krl": ["👉 Ботни бошлаш учун /start ни босинг", "♻️ Олдинги жойдан давом этяпмиз. Давом этинг 👇"],
    "qzq": ["👉 Ботты бастау үшін /start түймесін басыңыз", "♻️ Алдыңғы жерден жалғастырып жатырмыз. Жалғастырыңыз 👇"],
    "kg": ["👉 Ботту баштоо үчүн /start баскычын басыңыз", "♻️ Мурунку жерден улантып жатабыз. Уланта бериңиз 👇"],
    "ru": ["👉 Чтобы начать работу с ботом, нажмите /start", "♻️ Продолжаем с того места, где вы остановились. Продолжайте 👇"],
    "eng": ["👉 To start the bot, press /start", "♻️ Resuming from where you left off. Please continue 👇"]
}

(
    NAME,
    PHONE,
    LOCATION,
    USER_TRUCK_NAME,
    USER_TRUCK_KABINA,
    USER_TRUCK_PRITSEP,
    USER_TRUCK_KABINA_SELECT,
    USER_YONALISHI,
    MAIN_MENU,
    USER_HARAJATLAR,
    USER_VALYUTA_OZIQ_OVQAT,
    OZIQ_OVQAT_CHEK,
    USER_OZIQ_OVQAT,
    USER_STAYANKA_VALYUTA,
    USER_STAY_SUMMA,
    STAYANKA_CHEK,
    USER_TEL_VALYUTA,
    USER_TELEFON,
    USER_YOQIGI_VALYUTA,
    TELEFON_CHEK,
    USER_YOQILGI_1L_NARX_SAVE,
    USER_YOQILGI_UMUMIY_HAJMI,
    USER_TEXNIK_XARAJATLAR,
    YOQIGI_CHEK,
    USER_BALON_VALYUTA,
    USER_BALON,
    BALON_CHEK,
    USER_BALON_NARX_SAVE,
    USER_MOTOR_VALYUTA,
    USER_MOTOR_NARX_SAVE,
    USER_ANTFRIS_VALYUTA,
    USER_ANTFRIS_NARX_SAVE,
    ANTFRIS_CHEK,
    USER_AFTOL_VALYUTA,
    USER_AFTOL_NARX_SAVE,
    AFTOL_CHEK,
    USER_YANGI_YONALISHI,
    SETTINGS_MENU,
    TRANSPORTNI_JOYLASHUVI,
    USER_TRANSPORTNI,
    TRANSPORTNI_VALYUTA,
    YANGI_LOCATION



) = range(42)

(
    ADMIN_LANG_STATE,
    ADMIN_MENU,
    CAT_TRUCK_NAME,
    TRUCK_NAME_CATEGORY,
    TRUCK_NAME,
    PRODUCT_TRUCK_KABINA_DAVLAT,
    PRODUCT_TRUCK_KABINA_NOMERI,
    PRODUCT_TRUCK_KABINA_CATEGORY,
    PRODUCT_TRUCK_PRITSEP_NOMERI,
    PRODUCT_TRUCK_PRITSEP_DAVLAT
) = range(42, 52)

def resume_router(update: Update, context: CallbackContext):
    tg_id = update.effective_user.id

    if tg_id in Admin_ids:
        return

    user = db.get_user_lang(tg_id)
    if not user or not user.get("lang"):
        return

    state = db.get_user_state(tg_id)
    if not state:
        return

    if not update.message or not update.message.text:
        return


def start(update: Update, context: CallbackContext):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    if tg_id in Admin_ids:
        update.message.reply_text("⛔️ Siz foydalanuvchi emassiz!")
        return ConversationHandler.END

    if user and user.get("lang"):
        lang = user["lang"]
        state = db.get_user_state(tg_id)

        if state and state != MAIN_MENU:
            update.message.reply_text(USER_LANGUAGE[lang][1])

        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16])],
        ]

        update.message.reply_text(
            start_user[lang][11],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU

    keyboard = [
        [InlineKeyboardButton(text, callback_data=data)]
        for text, data in LANGUAGE_BUTTON["uz"]
    ]

    update.message.reply_text(
        BAZA["settings_language"]["uz"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    db.update_user_state(tg_id, NAME)
    return NAME

def set_language(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    lang = query.data.split("_")[1]
    tg_id = query.from_user.id

    db.add_lang(tg_id, lang)
    context.user_data["language"] = lang
    query.message.reply_text(start_user[lang][0])

    db.update_user_state(tg_id, NAME)
    return NAME


def get_name(update: Update, context: CallbackContext):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    if not user or not user.get("lang"):
        keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in LANGUAGE_BUTTON["uz"]]
        update.message.reply_text(
            BAZA["settings_language"]["uz"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        db.update_user_state(tg_id, NAME)
        return NAME
    lang = user["lang"]

    context.user_data["full_name"] = update.message.text
    context.user_data["username"] = update.effective_user.username

    keyboard = [[KeyboardButton(MENU_BUTTONS[lang][0], request_contact=True)]]

    update.message.reply_text(
        start_user[lang][1],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    db.update_user_state(tg_id, PHONE)
    return PHONE


def get_phone(update: Update, context: CallbackContext):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    if not user or not user.get("lang"):
        keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in LANGUAGE_BUTTON["uz"]]
        update.message.reply_text(
            BAZA["settings_language"]["uz"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        db.update_user_state(tg_id, NAME)
        return NAME
    lang = user["lang"]

    if not update.message.contact:
        update.message.reply_text(start_user[lang][2])
        db.update_user_state(tg_id, PHONE)
        return PHONE
    context.user_data["phone"] = update.message.contact.phone_number
    keyboard = [[KeyboardButton(MENU_BUTTONS[lang][1], request_location=True)]]
    update.message.reply_text(start_user[lang][3], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, LOCATION)
    return LOCATION


def get_location(update: Update, context: CallbackContext):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    if not update.message.location:
        update.message.reply_text(start_user[lang][4])
        db.update_user_state(tg_id, LOCATION)
        return LOCATION

    loc = update.message.location
    context.user_data["lat"] = loc.latitude
    context.user_data["lon"] = loc.longitude

    truck_name_category = db.get_truck_category()
    keyboard = []
    for idsi, name in truck_name_category:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=f"truck_{idsi}")])
    update.message.reply_text(start_user[lang][5],reply_markup=InlineKeyboardMarkup(keyboard))
    db.update_user_state(tg_id, USER_TRUCK_KABINA)
    return USER_TRUCK_KABINA


def user_truck_kabina_nomer_save(update, context):
    query = update.callback_query
    query.answer()

    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    if not user or not user.get("lang"):
        keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in LANGUAGE_BUTTON["uz"]]
        query.message.reply_text(
            BAZA["settings_language"]["uz"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        db.update_user_state(tg_id, NAME)
        return NAME

    lang = user["lang"]

    truck_id = query.data.split("_")[1]
    context.user_data["truck_nomi"] = db.get_all_kabina_nomer(truck_id)

    Truck_nomer_category = db.get_all_kabina_nomer(truck_id)

    if not Truck_nomer_category:
        query.message.reply_text(start_user[lang][7])
        db.update_user_state(tg_id, ConversationHandler.END)
        return ConversationHandler.END

    keyboard = []
    context.user_data["truck_kabina_map"] = {}

    for id, bayroq, nomer in Truck_nomer_category:
        text = f"{bayroq} {nomer}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"kabina_{id}")])
        context.user_data["truck_kabina_map"][str(id)] = text

    query.message.reply_text(
        start_user[lang][6],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    db.update_user_state(tg_id, USER_TRUCK_KABINA_SELECT)
    return USER_TRUCK_KABINA_SELECT

def user_pritsep_nomer(update, context):
    query = update.callback_query
    query.answer()

    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    kabina_id = query.data.split("_")[1]

    context.user_data["truck_kabina_nomer"] = context.user_data["truck_kabina_map"].get(kabina_id)

    pritsep_list = db.get_all_pritsep_numbers()

    if not pritsep_list:
        query.message.reply_text(start_user[lang][8])
        db.update_user_state(tg_id, USER_TRUCK_PRITSEP)
        return USER_TRUCK_PRITSEP

    keyboard = []
    context.user_data["user_pritsep_map"] = {}

    for pid, davlat, nomer in pritsep_list:
        text = f"{davlat} {nomer}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"pritsep_{pid}")])
        context.user_data["user_pritsep_map"][str(pid)] = text

    query.message.reply_text(
        start_user[lang][8],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    db.update_user_state(tg_id,USER_TRUCK_PRITSEP)
    return USER_TRUCK_PRITSEP


def user_pritsep_save(update, context):
    query = update.callback_query
    query.answer()
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    pritsep_id = query.data.split("_")[1]
    pritsep_nomer = context.user_data["user_pritsep_map"].get(pritsep_id)
    context.user_data["truck_pritsep_nomer"] = pritsep_nomer

    if not pritsep_nomer:
        query.message.reply_text(start_user[lang][7])
        db.update_user_state(tg_id, USER_TRUCK_PRITSEP)
        return USER_TRUCK_PRITSEP

    keyboard = [
        [InlineKeyboardButton(MENU_BUTTONS[lang][2], callback_data="yonalish_1")],
        [InlineKeyboardButton(MENU_BUTTONS[lang][3], callback_data="yonalish_2")],
        [InlineKeyboardButton(MENU_BUTTONS[lang][4], callback_data="yonalish_3")],
        [InlineKeyboardButton(MENU_BUTTONS[lang][5], callback_data="yonalish_4")],
        [InlineKeyboardButton(MENU_BUTTONS[lang][6], callback_data="yonalish_5")],
        [InlineKeyboardButton(MENU_BUTTONS[lang][7], callback_data="yonalish_6")],
        [InlineKeyboardButton(MENU_BUTTONS[lang][8], callback_data="yonalish_7")],
        [InlineKeyboardButton(MENU_BUTTONS[lang][9], callback_data="yonalish_8")],
    ]

    query.message.reply_text(start_user[lang][9], reply_markup=InlineKeyboardMarkup(keyboard))
    db.update_user_state(tg_id,USER_YONALISHI)
    return USER_YONALISHI


def yonalish_save(update, context):
    query = update.callback_query
    query.answer()

    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    yonalish_id = query.data.split("_")[1]

    yonalish_map = {
        "1": MENU_BUTTONS[lang][2],
        "2": MENU_BUTTONS[lang][3],
        "3": MENU_BUTTONS[lang][4],
        "4": MENU_BUTTONS[lang][5],
        "5": MENU_BUTTONS[lang][6],
        "6": MENU_BUTTONS[lang][7],
        "7": MENU_BUTTONS[lang][8],
        "8": MENU_BUTTONS[lang][9],
    }

    context.user_data["yonalishi_map"] = yonalish_map.get(yonalish_id)

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]

    query.message.reply_text(
        start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def menu_buttonslar(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    text = update.message.text
    if text == MENU_BUTTONS[lang][10]:
        keyboard=[
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][5]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][6])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][7])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_HARAJATLAR)
        return USER_HARAJATLAR

    if text == MENU_BUTTONS[lang][11]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(
            USER_MENU_BUYRUQLAR[lang][0],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        db.update_user_state(tg_id, USER_YOQIGI_VALYUTA)
        return USER_YOQIGI_VALYUTA

    if text == MENU_BUTTONS[lang][12]:
        keyboard=[
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][8]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][9])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][11]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][12])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_TEXNIK_XARAJATLAR)
        return USER_TEXNIK_XARAJATLAR

    if text == MENU_BUTTONS[lang][13]:
        keyboard=[
            [KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][0]), KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][1])],
            [KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][2]), KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][3])],
            [KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][4]), KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][5])],
            [KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][6]), KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][7])],
            [KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][8]), KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][9])],
            [KeyboardButton(MENU_TRANSPORTNI_JOYLASHUVI[lang][10])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][22], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, TRANSPORTNI_JOYLASHUVI)
        return TRANSPORTNI_JOYLASHUVI


    if text == MENU_BUTTONS[lang][14]:
        keyboard=[
            [KeyboardButton(MENU_BUTTONS[lang][2]), KeyboardButton(MENU_BUTTONS[lang][3])],
            [KeyboardButton(MENU_BUTTONS[lang][4]), KeyboardButton(MENU_BUTTONS[lang][5])],
            [KeyboardButton(MENU_BUTTONS[lang][6]), KeyboardButton(MENU_BUTTONS[lang][7])],
            [KeyboardButton(MENU_BUTTONS[lang][8]), KeyboardButton(MENU_BUTTONS[lang][9])],
            [KeyboardButton(YANGI_YONALISH[lang][0]), KeyboardButton(YANGI_YONALISH[lang][1])],
            [KeyboardButton(YANGI_YONALISH[lang][2]), KeyboardButton(YANGI_YONALISH[lang][3])],
            [KeyboardButton(YANGI_YONALISH[lang][4]), KeyboardButton(YANGI_YONALISH[lang][5])],
            [KeyboardButton(YANGI_YONALISH[lang][6]), KeyboardButton(YANGI_YONALISH[lang][7])],
            [KeyboardButton(YANGI_YONALISH[lang][8]), KeyboardButton(YANGI_YONALISH[lang][9])],
            [KeyboardButton(YANGI_YONALISH[lang][10]), KeyboardButton(YANGI_YONALISH[lang][11])],
            [KeyboardButton(YANGI_YONALISH[lang][12]), KeyboardButton(YANGI_YONALISH[lang][13])],
            [KeyboardButton(YANGI_YONALISH[lang][14]), KeyboardButton(YANGI_YONALISH[lang][15])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_YANGI_YONALISHI)
        return USER_YANGI_YONALISHI


    if text == MENU_BUTTONS[lang][16]:
        keyboard=[
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][14])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, SETTINGS_MENU)
        return SETTINGS_MENU

    if text == USER_MENU_ICHKI_BUTTONS[lang][16]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][17], request_location=True)],
         ]
        update.message.reply_text(start_user[lang][3], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, YANGI_LOCATION)
        return YANGI_LOCATION

    if text == USER_MENU_ICHKI_BUTTONS[lang][15]:
        xarajatlar_save(tg_id, context)
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][15], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return MAIN_MENU

def xarajatlar_save(tg_id, context):
    data = context.user_data
    db.add_user(
        tg_id=tg_id,
        full_name=data.get("full_name"),
        username=data.get("username"),
        phone=data.get("phone"),
        lat=data.get("lat"),
        lon=data.get("lon"),
        truck_nomi=str(data.get("truck_nomi")) if data.get("truck_nomi") else None,
        truck_kabina_nomer=str(data.get("truck_kabina_nomer")) if data.get("truck_kabina_nomer") else None,
        truck_pritsep_nomer=str(data.get("truck_pritsep_nomer")) if data.get("truck_pritsep_nomer") else None,
        yonalishi_map=str(data.get("yonalishi_map")) if data.get("yonalishi_map") else None,
        yangi_yonalish=data.get("yangi_yonalish"),
        lati=data.get("lati", "0"),
        longi=data.get("longi", "0"),
        oziq_ovqat_valyuta=data.get("oziq_ovqat_valyuta"),
        oziq_ovqat_uchun=data.get("oziq_ovqat_narxi"),
        stayanka_valyuta=data.get("stayanka_valyuta"),
        stayanka_uchun=data.get("stayanka_narxi"),
        tel_valyuta=data.get("tel_valyuta"),
        tel_uchun=data.get("tel_narxi"),
        yoqilgi_valyuta=data.get("yoqilgi_valyuta"),
        yoqilgi_1l_narxi=data.get("yoqilgi_1l_narxi"),
        yoqilgi_umumiy_hajmi=data.get("yoqilgi_umumiy_hajmi"),
        yoqilgi_umumiy_narx=data.get("yoqilgi_umumiy_narx"),
        balon_valyuta=data.get("balon_valyuta"),
        balon_uchun=data.get("balon_narxi"),
        motor_valyuta=data.get("motor_valyuta"),
        motor_uchun=data.get("motor_narxi"),
        aftol_valyuta=data.get("aftol_valyuta"),
        aftol_uchun=data.get("aftol_narxi"),
        antfris_valyuta=data.get("antfris_valyuta"),
        antfris_uchun=data.get("antfris_narxi"),
        transport_toroz_joylashuvi=data.get("transport_toroz_joylashuvi"),
        transportni_valyuta=data.get("transportni_valyuta"),
        transportni_toroz_uchun=data.get("transportni_narxi")
    )

def user_kunlik_harajatlar(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)
    lang = user["lang"]

    text = update.message.text
    if text == USER_MENU_ICHKI_BUTTONS[lang][5]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])],
        ]
        update.message.reply_text(
            USER_MENU_BUYRUQLAR[lang][0],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        db.update_user_state(tg_id, USER_VALYUTA_OZIQ_OVQAT)
        return USER_VALYUTA_OZIQ_OVQAT

    if text == USER_MENU_ICHKI_BUTTONS[lang][6]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])],
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0],reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        db.update_user_state(tg_id, USER_STAYANKA_VALYUTA)
        return USER_STAYANKA_VALYUTA

    if text == USER_MENU_ICHKI_BUTTONS[lang][7]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]),
             KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]),
             KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]

        update.message.reply_text(
            USER_MENU_BUYRUQLAR[lang][0],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        db.update_user_state(tg_id, USER_TEL_VALYUTA)
        return USER_TEL_VALYUTA

    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU

def save_oziq_valyuta(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    text = update.message.text

    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][5]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][6])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][7])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(
            USER_MENU_BUYRUQLAR[lang][1],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        db.update_user_state(tg_id, USER_HARAJATLAR)
        return USER_HARAJATLAR

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_VALYUTA_OZIQ_OVQAT)
        return USER_VALYUTA_OZIQ_OVQAT

    context.user_data["oziq_ovqat_valyuta"] = valyuta_map[text]

    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][2] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_OZIQ_OVQAT)
    return USER_OZIQ_OVQAT

def oziq_ovqat_rasxod(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    text = update.message.text

    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(
            USER_MENU_BUYRUQLAR[lang][0],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        db.update_user_state(tg_id, USER_VALYUTA_OZIQ_OVQAT)
        return USER_VALYUTA_OZIQ_OVQAT

    try:
        context.user_data["oziq_ovqat_narxi"] = int(text)
        update.message.reply_text(CHEK_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, OZIQ_OVQAT_CHEK)
        return OZIQ_OVQAT_CHEK

    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_OZIQ_OVQAT)
        return USER_OZIQ_OVQAT

def oziq_ovqat_chek(update: Update, context: CallbackContext):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    if not update.message.photo:
        update.message.reply_text(CHEK_BUYRUQLAR[lang][7])
        db.update_user_state(tg_id, OZIQ_OVQAT_CHEK)
        return OZIQ_OVQAT_CHEK

    user_id = update.effective_user.id
    fil_id = update.message.photo[-1].file_id

    db.add_chek(user_id, "oziq_ovqat_chek", fil_id)
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][26])

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]

    update.message.reply_text(
        start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU



def stayanka_valyuta_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    text = update.message.text

    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][5]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][6])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][7])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_HARAJATLAR)
        return USER_HARAJATLAR

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_STAYANKA_VALYUTA)
        return USER_STAYANKA_VALYUTA

    context.user_data["stayanka_valyuta"] = valyuta_map[text]

    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][3] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_STAY_SUMMA)
    return USER_STAY_SUMMA

def stayanka_summa_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    text = update.message.text
    try:
        context.user_data["stayanka_narxi"] = int(text)
        update.message.reply_text(CHEK_BUYRUQLAR[lang][1])
        db.update_user_state(tg_id, STAYANKA_CHEK)
        return STAYANKA_CHEK
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_STAY_SUMMA)
        return USER_STAY_SUMMA

def stayanka_chek(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    if not update.message.photo:
        update.message.reply_text(CHEK_BUYRUQLAR[lang][8])
        db.update_user_state(tg_id, STAYANKA_CHEK)
        return STAYANKA_CHEK
    user_id = update.effective_user.id
    fil_id = update.message.photo[-1].file_id

    db.add_chek(user_id, "stayanka_chek", fil_id)
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][12])

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]

    update.message.reply_text(
        start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def telefon_valyuta_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    text = update.message.text
    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][5]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][6])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][7])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][13])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_HARAJATLAR)
        return USER_HARAJATLAR

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_TEL_VALYUTA)
        return USER_TEL_VALYUTA

    context.user_data["tel_valyuta"] = valyuta_map[text]

    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][4] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_TELEFON)
    return USER_TELEFON

def telefon_summa_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    try:
        context.user_data["tel_narxi"] = int(update.message.text)
        update.message.reply_text(CHEK_BUYRUQLAR[lang][2])
        db.update_user_state(tg_id, TELEFON_CHEK)
        return TELEFON_CHEK
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_TELEFON)
        return USER_TELEFON

def telefon_chek(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    if not update.message.photo:
        update.message.reply_text(CHEK_BUYRUQLAR[lang][9])
        db.update_user_state(tg_id, TELEFON_CHEK)
        return TELEFON_CHEK
    user_id = update.effective_user.id
    fil_id = update.message.photo[-1].file_id

    db.add_chek(user_id, "telefon_chek", fil_id)
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][13])

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]
    update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU


def yoqilgi_valyuta(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    text = update.message.text

    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(start_user[lang][11],reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_YOQIGI_VALYUTA)
        return USER_YOQIGI_VALYUTA

    context.user_data["yoqilgi_valyuta"] = valyuta_map[text]
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][5] + f" ({valyuta_map[text]})")
    db.update_user_state(tg_id, USER_YOQILGI_1L_NARX_SAVE)
    return USER_YOQILGI_1L_NARX_SAVE



def yoqilgi_1l_narx(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    try:
        context.user_data["yoqilgi_1l_narxi"] = int(update.message.text)
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][6])
        db.update_user_state(tg_id, USER_YOQILGI_UMUMIY_HAJMI)
        return USER_YOQILGI_UMUMIY_HAJMI
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_YOQILGI_1L_NARX_SAVE)
        return USER_YOQILGI_1L_NARX_SAVE



def yoqilgi_umumiy_hajmi(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    if not user or not user.get("lang"):
        keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in LANGUAGE_BUTTON["uz"]]
        update.message.reply_text(
            BAZA["settings_language"]["uz"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        db.update_user_state(tg_id, NAME)
        return NAME
    lang = user["lang"]

    try:
        litre = context.user_data.get("yoqilgi_1l_narxi", 0)
        hajm = int(update.message.text)
        context.user_data["yoqilgi_umumiy_hajmi"] = hajm
        context.user_data["yoqilgi_umumiy_narx"] = litre * hajm
        update.message.reply_text(CHEK_BUYRUQLAR[lang][3])
        db.update_user_state(tg_id, YOQIGI_CHEK)
        return YOQIGI_CHEK
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_YOQILGI_UMUMIY_HAJMI)
        return USER_YOQILGI_UMUMIY_HAJMI

def yoqilgi_chek(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    if not update.message.photo:
        update.message.reply_text(CHEK_BUYRUQLAR[lang][10])
        db.update_user_state(tg_id, YOQIGI_CHEK)
        return YOQIGI_CHEK
    user_id = update.effective_user.id
    fil_id = update.message.photo[-1].file_id

    db.add_chek(user_id, "yoqilgi_chek", fil_id)
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][14])
    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]
    update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def texnik_harajatlar(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    text = update.message.text
    if text ==USER_MENU_ICHKI_BUTTONS[lang][8]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_BALON_VALYUTA)
        return USER_BALON_VALYUTA

    if text ==USER_MENU_ICHKI_BUTTONS[lang][9]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][1], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_MOTOR_VALYUTA)
        return USER_MOTOR_VALYUTA


    if text == USER_MENU_ICHKI_BUTTONS[lang][11]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0],
                                  reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_ANTFRIS_VALYUTA)
        return USER_ANTFRIS_VALYUTA

    if text == USER_MENU_ICHKI_BUTTONS[lang][12]:
        keyboard = [
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])]
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0],
                                  reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, USER_AFTOL_VALYUTA)
        return USER_AFTOL_VALYUTA

    if text ==USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(start_user[lang][11],reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU


def balon_valyuta_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    text = update.message.text

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_BALON_VALYUTA)
        return USER_BALON_VALYUTA


    context.user_data["balon_valyuta"] = valyuta_map[text]

    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][7] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_BALON_NARX_SAVE)
    return USER_BALON_NARX_SAVE

def balon_narxi_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    try:
        context.user_data["balon_narxi"] = int(update.message.text)
        update.message.reply_text(CHEK_BUYRUQLAR[lang][4])
        db.update_user_state(tg_id, BALON_CHEK)
        return BALON_CHEK
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_BALON_NARX_SAVE)
        return USER_BALON_NARX_SAVE

def balon_chek(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    if not update.message.photo:
        update.message.reply_text(CHEK_BUYRUQLAR[lang][11])
        db.update_user_state(tg_id, BALON_CHEK)
        return BALON_CHEK
    user_id = update.effective_user.id
    fil_id = update.message.photo[-1].file_id

    db.add_chek(user_id, "balon_chek", fil_id)
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][17])
    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]
    update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def motor_valyuta(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    text = update.message.text

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_MOTOR_VALYUTA)
        return USER_MOTOR_VALYUTA

    context.user_data["motor_valyuta"] = valyuta_map[text]

    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][8] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_MOTOR_NARX_SAVE)
    return USER_MOTOR_NARX_SAVE

def motor_narxi_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    try:
        context.user_data["motor_narxi"] = int(update.message.text)
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][18], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_MOTOR_NARX_SAVE)
        return USER_MOTOR_NARX_SAVE


def anfris_valyuta(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }
    text = update.message.text
    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_ANTFRIS_VALYUTA)
        return USER_ANTFRIS_VALYUTA

    context.user_data["antfris_valyuta"] = valyuta_map[text]
    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][10] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_ANTFRIS_NARX_SAVE)
    return USER_ANTFRIS_NARX_SAVE

def antfris_narx_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]

    try:
        context.user_data["antfris_narxi"] = int(update.message.text)
        update.message.reply_text(CHEK_BUYRUQLAR[lang][5])
        db.update_user_state(tg_id, ANTFRIS_CHEK)
        return ANTFRIS_CHEK
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_ANTFRIS_NARX_SAVE)
        return USER_ANTFRIS_NARX_SAVE

def antsfris_chek(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    if not user or not user.get("lang"):
        keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in LANGUAGE_BUTTON["uz"]]
        update.message.reply_text(
            BAZA["settings_language"]["uz"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        db.update_user_state(tg_id, NAME)
        return NAME

    lang = user["lang"]

    if not update.message.photo:
        update.message.reply_text(CHEK_BUYRUQLAR[lang][12])
        db.update_user_state(tg_id, ANTFRIS_CHEK)
        return ANTFRIS_CHEK
    user_id = update.effective_user.id
    fil_id = update.message.photo[-1].file_id

    db.add_chek(user_id, "antfris_chek", fil_id)
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][19])

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]
    update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def aftol_valyuta(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    if not user or not user.get("lang"):
        keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in LANGUAGE_BUTTON["uz"]]
        update.message.reply_text(
            BAZA["settings_language"]["uz"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return NAME
    lang = user["lang"]

    text = update.message.text
    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, USER_AFTOL_VALYUTA)
        return USER_AFTOL_VALYUTA

    context.user_data["aftol_valyuta"] = valyuta_map[text]

    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][11] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_AFTOL_NARX_SAVE)
    return USER_AFTOL_NARX_SAVE

def aftol_narx_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    try:
        context.user_data["aftol_narxi"] = int(update.message.text)
        update.message.reply_text(CHEK_BUYRUQLAR[lang][6])
        db.update_user_state(tg_id, AFTOL_CHEK)
        return AFTOL_CHEK
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_AFTOL_NARX_SAVE)
        return USER_AFTOL_NARX_SAVE

def aftol_chek(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    user_id = update.effective_user.id
    if not update.message.photo:
        update.message.reply_text(CHEK_BUYRUQLAR[lang][13])
        db.update_user_state(tg_id, AFTOL_CHEK)
        return AFTOL_CHEK

    fil_id = update.message.photo[-1].file_id

    db.add_chek(user_id, "aftol_chek", fil_id)
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][20])

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]
    update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def transpootrni_rasxod(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    text = update.message.text
    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU

    context.user_data["transport_toroz_joylashuvi"] = text
    keyboard = [
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][0]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][1])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][2]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][3])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][4])]
    ]
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, TRANSPORTNI_VALYUTA)
    return TRANSPORTNI_VALYUTA

def transportni_valyuta(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    text = update.message.text

    valyuta_map = {
        USER_MENU_ICHKI_BUTTONS[lang][0]: "UZS",
        USER_MENU_ICHKI_BUTTONS[lang][1]: "KZT",
        USER_MENU_ICHKI_BUTTONS[lang][2]: "KGS",
        USER_MENU_ICHKI_BUTTONS[lang][3]: "RUB",
        USER_MENU_ICHKI_BUTTONS[lang][4]: "USD",
    }

    if text not in valyuta_map:
        update.message.reply_text(USER_MENU_BUYRUQLAR[lang][0])
        db.update_user_state(tg_id, TRANSPORTNI_VALYUTA)
        return TRANSPORTNI_VALYUTA

    context.user_data["transportni_valyuta"] = valyuta_map[text]
    update.message.reply_text(
        USER_MENU_BUYRUQLAR[lang][22] + f" ({valyuta_map[text]})"
    )
    db.update_user_state(tg_id, USER_TRANSPORTNI)
    return USER_TRANSPORTNI

def Transportni_narx_save(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    try:
        context.user_data["transportni_narxi"] = int(update.message.text)
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU
    except ValueError:
        update.message.reply_text(ADMIN_USER[lang][11])
        db.update_user_state(tg_id, USER_TRANSPORTNI)
        return USER_TRANSPORTNI


def settings_menu(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)

    lang = user["lang"]
    text = update.message.text

    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU

    if text == USER_MENU_ICHKI_BUTTONS[lang][14]:
        keyboard = [
            [InlineKeyboardButton(text, callback_data=data)]
            for text, data in LANGUAGE_BUTTON[lang]]

        update.message.reply_text(
            BAZA["settings_language"][lang],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        db.update_user_state(tg_id, SETTINGS_MENU)
        return SETTINGS_MENU


def settings_menu_save(update, context):
    query = update.callback_query
    query.answer()

    lang = query.data.split("_")[1]
    tg_id = query.from_user.id

    db.update_user_lang(tg_id, lang)
    context.user_data["language"] = lang

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]

    query.message.reply_text(start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def user_yangi_yonalish(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)


    lang = user["lang"]
    text = update.message.text

    if text == USER_MENU_ICHKI_BUTTONS[lang][13]:
        keyboard = [
            [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
            [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
            [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
            [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
        ]
        update.message.reply_text(start_user[lang][11], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        db.update_user_state(tg_id, MAIN_MENU)
        return MAIN_MENU

    context.user_data["yangi_yonalish"] = update.message.text

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][24], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU

def yangi_location(update, context):
    tg_id = update.effective_user.id
    user = db.get_user_lang(tg_id)
    lang = user["lang"]

    if not update.message.location:
        update.message.reply_text(start_user[lang][4])
        return YANGI_LOCATION

    loca = update.message.location
    context.user_data["lati"] = loca.latitude
    context.user_data["longi"] = loca.longitude
    update.message.reply_text(USER_MENU_BUYRUQLAR[lang][25])

    keyboard = [
        [KeyboardButton(MENU_BUTTONS[lang][10]), KeyboardButton(MENU_BUTTONS[lang][11])],
        [KeyboardButton(MENU_BUTTONS[lang][12]), KeyboardButton(MENU_BUTTONS[lang][13])],
        [KeyboardButton(MENU_BUTTONS[lang][14]), KeyboardButton(MENU_BUTTONS[lang][16])],
        [KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][16]), KeyboardButton(USER_MENU_ICHKI_BUTTONS[lang][15])],
    ]

    update.message.reply_text(
        start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    db.update_user_state(tg_id, MAIN_MENU)
    return MAIN_MENU


def bind_group(update: Update, context: CallbackContext):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return update.message.reply_text("❌ Bu komanda faqat guruhda ishlaydi!")

    context.bot_data["BOUND_GROUP_ID"] = chat.id
    update.message.reply_text("✅ Guruh muvaffaqiyatli ulandi!")

def gp_bot(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message

    if user.id not in Admin_ids:
        return message.reply_text("⛔️ Siz admin emassiz!")

    group_id = context.bot_data.get("BOUND_GROUP_ID")
    if not group_id:
        return message.reply_text(
            "❌ Guruhga bot ulanmagan. /bind komandasi yordamida ulang."
        )

    try:
        users = db.get_all_users()
        print("USERS:", len(users))
        if not users:
            return message.reply_text("❌ Hozircha user ma’lumotlari mavjud emas.")
        sent = 0

        for category in users:
            if not category.get("tg_id"):
                continue

            send_user_to_group(update, context, category, group_id)
            sent += 1
        message.reply_text(f"✅ {sent} ta foydalanuvchi guruhga yuborildi!")

    except Exception as e:
        message.reply_text(f"❌ Xatolik: {e}")

def send_user_to_group(update: Update, context: CallbackContext, category, group_id):
    user_id = category.get("tg_id") or ""
    first_data = db.get_user_first(user_id)

    username = first_data.get("username") if first_data else "❌"
    ism = first_data.get("full_name") if first_data else "❌"
    telefon = first_data.get("phone") if first_data else "❌"
    kabina = first_data.get("truck_kabina_nomer") if first_data else "❌"
    pritsep = first_data.get("truck_pritsep_nomer") if first_data else "❌"
    Yonalish = first_data.get("yonalishi_map") if first_data else "❌"
    yangi_yonalish = category.get("yangi_yonalish") or "❌"
    Lat = category.get("lat") or "0"
    Lon = category.get("lon") or "0"
    Lati = category.get("lati") or "0"
    Long = category.get("longi") or "0"
    oziq_ovqat_valyuta = category.get("oziq_ovqat_valyuta") or ''
    oziq_ovqat = category.get("oziq_ovqat_uchun") or "❌"

    stayanka_valyuta = category.get("stayanka_valyuta") or ''
    stayanka = category.get("stayanka_uchun") or "❌"

    tel_valyuta = category.get("tel_valyuta") or ''
    tel = category.get("tel_uchun") or "❌"

    yoqilgi_valyut = category.get("yoqilgi_valyuta") or ''
    yoqilgi_1l_narxi = category.get("yoqilgi_1l_narxi") or "❌"
    yoqilgi_umumiy_hajm = category.get("yoqilgi_umumiy_hajmi") or "❌"
    yoqilgi_umumiy_narx = category.get("yoqilgi_umumiy_narx") or "❌"

    balon_valyuta = category.get("balon_valyuta") or ''
    balon_uchun = category.get("balon_uchun") or "❌"

    motor_valyut = category.get("motor_valyuta") or ''
    motor_uchun = category.get("motor_uchun") or "❌"

    aftol_valyut = category.get("aftol_valyuta") or ''
    aftol_uchun = category.get("aftol_uchun") or "❌"

    antfris_valyuta = category.get("antfris_valyuta") or ''
    antfris_uchun = category.get("antfris_uchun") or "❌"

    transportni_valyut = category.get("transportni_valyuta") or ''
    transport_toroz_joylashuvi = category.get("transport_toroz_joylashuvi") or "❌"
    transportni_toroz_uchun = category.get("transportni_toroz_uchun") or "❌"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📍 Location",
                url=f"https://yandex.uz/maps/?ll={Lon},{Lat}&z=12"
            ),
            InlineKeyboardButton(
                "📍 Yangi Location",
                url=f"https://yandex.uz/maps/?ll={Long},{Lati}&z=12"
            )
        ]
    ])

    text = (
        f"📦 YANGI HAYDOVCHI\n\n"
        f"🆔 User ID: {user_id}\n\n"
        f"👤 Username: @{username}\n\n"
        f"👤 Haydovchi: {ism}\n\n"
        f"☎️ Telefon: {telefon}\n\n"
        f"🚛 Kabina nomer: {kabina}\n\n"
        f"🚛 Pritsep nomer: {pritsep}\n\n"
        f"🛣 Yonalish: {Yonalish}\n\n"
        f"🛣 Yangi yonalish: {yangi_yonalish}\n\n"
        f"🍛 Oziq ovqat: {oziq_ovqat_valyuta} {oziq_ovqat}\n\n"
        f"🅿️ Stayanka: {stayanka_valyuta} {stayanka}\n\n"
        f"📱 Telefon: {tel_valyuta} {tel}\n\n"
        f"🛢 Yoqilgi 1l narxi: {yoqilgi_valyut} {yoqilgi_1l_narxi}\n\n"
        f"🛢 Yoqilg'i Umumiy hajmi: {yoqilgi_umumiy_hajm}\n\n"
        f"💵 Yoqilgi umumiy narxi: {yoqilgi_valyut} {yoqilgi_umumiy_narx}\n\n"
        f"🛞 Balon: {balon_valyuta} {balon_uchun}\n\n"
        f"🚛 Motor: {motor_valyut} {motor_uchun}\n\n"
        f"🛢 Antfris: {antfris_valyuta} {antfris_uchun}\n\n"
        f"🛢 Aftol: {aftol_valyut} {aftol_uchun}\n\n"
        f"📍 Transportni taroz joylashuvi: {transport_toroz_joylashuvi}\n\n"
        f"🚛 Transportni taroz narxi: {transportni_valyut} {transportni_toroz_uchun}\n\n"
    )

    photos_list = db.get_all_chek(user_id)

    if photos_list:
        chunk_size = 10
        for i in range(0, len(photos_list), chunk_size):
            chunk = photos_list[i:i + chunk_size]
            media_group = [InputMediaPhoto(photo) for photo in chunk]
            if i == 0:
                media_group[0].caption = text
            context.bot.send_media_group(chat_id=group_id, media=media_group)

        context.bot.send_message(chat_id=group_id, text="👇 Shafyor lokatsiyalari", reply_markup=keyboard)
    else:
        context.bot.send_message(chat_id=group_id, text=text, reply_markup=keyboard)


def admin_id(user_id):
    return user_id in Admin_ids


def admin(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if user_id not in Admin_ids:
        update.message.reply_text("⛔️ Siz admin emassiz!")
        return ConversationHandler.END

    if user_id in admin_language:
        lang = admin_language[user_id]
        update.message.reply_text(ADMIN_USER[lang][1])
        return ADMIN_MENU

    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in LANGUAGE_BUTTON["uz"]]
    update.message.reply_text(
        "🇺🇿  🇵🇼  🇰🇬  🇷🇺  🇺🇸\n uz qzq kg ru us",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ADMIN_LANG_STATE


def admin_set_language(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    lang = query.data.split("_")[1]

    admin_language[user_id] = lang

    query.message.reply_text(ADMIN_USER[lang][0])
    return ADMIN_MENU


def admin_login(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if user_id not in Admin_ids:
        update.message.reply_text("⛔️ Siz admin emassiz!")
        return ConversationHandler.END

    lang = admin_language.get(user_id, "uz")
    admin_language[user_id] = lang

    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 2 or parts[0] != "/admin":
        update.message.reply_text(ADMIN_USER[lang][1])
        return ADMIN_MENU

    password = parts[1]

    if password != Admin_password:
        update.message.reply_text(ADMIN_USER[lang][2])
        return ADMIN_MENU

    keyboard = [
        [KeyboardButton(ADMIN_BUTTONS[lang][5])],
        [KeyboardButton(ADMIN_BUTTONS[lang][6])],
        [KeyboardButton(ADMIN_BUTTONS[lang][7])]
    ]
    update.message.reply_text(
        ADMIN_USER[lang][3],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ADMIN_MENU

def show_admin_menu(update, lang):
    keyboard = [
        [KeyboardButton(ADMIN_BUTTONS[lang][5])],
        [KeyboardButton(ADMIN_BUTTONS[lang][6])],
        [KeyboardButton(ADMIN_BUTTONS[lang][7])]
    ]
    update.message.reply_text(
        ADMIN_USER[lang][3],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


def admin_select(update, context):
    user_id = update.effective_user.id
    lang = admin_language.get(user_id)
    text = update.message.text.strip()

    if text == ADMIN_BUTTONS[lang][7]:
        keyboard = [
            [InlineKeyboardButton(ADMIN_BUTTONS[lang][0], callback_data="pritsep_country_uz")],
            [InlineKeyboardButton(ADMIN_BUTTONS[lang][1], callback_data="pritsep_country_qzq")],
            [InlineKeyboardButton(ADMIN_BUTTONS[lang][2], callback_data="pritsep_country_kg")],
            [InlineKeyboardButton(ADMIN_BUTTONS[lang][3], callback_data="pritsep_country_ru")],
            [InlineKeyboardButton(ADMIN_BUTTONS[lang][4], callback_data="pritsep_country_eng")],
        ]
        update.message.reply_text(ADMIN_USER[lang][12],
                                  reply_markup=InlineKeyboardMarkup(keyboard, resize_keyboard=True)
                                  )
        return PRODUCT_TRUCK_PRITSEP_DAVLAT

    if text == ADMIN_BUTTONS[lang][5].strip():
        update.message.reply_text(ADMIN_USER[lang][4])
        return TRUCK_NAME

    if text == ADMIN_BUTTONS[lang][6]:
        truck_categories = db.get_truck_category()
        keyboard = []

        for idsi, name in truck_categories:
            key = f"{name}"
            keyboard.append([key])
            context.user_data[f"admin_truck_cat_{key}"] = idsi
        update.message.reply_text(
            ADMIN_USER[lang][6],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return TRUCK_NAME_CATEGORY


def truck_name(update, context):
    user_id = update.effective_user.id
    lang = admin_language.get(user_id)

    db.add_truck_category(update.message.text.upper())
    update.message.reply_text(ADMIN_USER[lang][5])
    keyboard = [
        [KeyboardButton(ADMIN_BUTTONS[lang][5])],
        [KeyboardButton(ADMIN_BUTTONS[lang][6])],
        [KeyboardButton(ADMIN_BUTTONS[lang][7])]
    ]
    update.message.reply_text(
        start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ADMIN_MENU


def truck_kabina_category(update, context):
    user_id = update.effective_user.id
    lang = admin_language.get(user_id)

    cid = context.user_data.get(f"admin_truck_cat_{update.message.text}")
    if not cid:
        update.message.reply_text(ADMIN_USER[lang][6])
        return TRUCK_NAME_CATEGORY

    context.user_data["truck_kabina_cat"] = cid

    keyboard = [
        [InlineKeyboardButton(ADMIN_BUTTONS[lang][0], callback_data="kabina_country_uz")],
        [InlineKeyboardButton(ADMIN_BUTTONS[lang][1], callback_data="kabina_country_qzq")],
        [InlineKeyboardButton(ADMIN_BUTTONS[lang][2], callback_data="kabina_country_kg")],
        [InlineKeyboardButton(ADMIN_BUTTONS[lang][3], callback_data="kabina_country_ru")],
        [InlineKeyboardButton(ADMIN_BUTTONS[lang][4], callback_data="kabina_country_eng")],
    ]
    update.message.reply_text(
        ADMIN_USER[lang][7],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PRODUCT_TRUCK_KABINA_DAVLAT


def truck_kabina_davlat_nomer(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    lang = admin_language.get(user_id)

    country_code = query.data.split("_")[-1]
    context.user_data["truck_davlat_nomeri"] = country_code

    query.message.reply_text(ADMIN_USER[lang][9])
    return PRODUCT_TRUCK_KABINA_NOMERI


def truck_kabina_davlat_nomer_save(update, context):
    user_id = update.effective_user.id
    lang = admin_language.get(user_id)

    kabina_nomer = update.message.text
    cat_id = context.user_data.get("truck_kabina_cat")
    country_code = context.user_data.get("truck_davlat_nomeri")

    if not cat_id or not country_code:
        update.message.reply_text(ADMIN_USER[lang][11])
        return ADMIN_MENU

    db.add_truck_nomer(
        cat_id=cat_id,
        kabina_nomer_davlat=country_code,
        truck_kabina_nomer=kabina_nomer
    )

    update.message.reply_text(ADMIN_USER[lang][10])
    keyboard = [
        [KeyboardButton(ADMIN_BUTTONS[lang][5])],
        [KeyboardButton(ADMIN_BUTTONS[lang][6])],
        [KeyboardButton(ADMIN_BUTTONS[lang][7])]
    ]
    update.message.reply_text(
        start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ADMIN_MENU


def truck_pritsep_davlat_nomer(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    lang = admin_language.get(user_id)
    country_code_pritsep = query.data.split("_")[-1]
    context.user_data["truck_pritsep_davlat_nomeri"] = country_code_pritsep
    query.message.reply_text(ADMIN_USER[lang][13])
    return PRODUCT_TRUCK_PRITSEP_NOMERI


def truck_pritsep_davlat_nomer_save(update, context):
    user_id = update.effective_user.id
    lang = admin_language.get(user_id)

    pritsep_nomer = update.message.text
    country_code_pritsep = context.user_data.get("truck_pritsep_davlat_nomeri")
    db.add_truck_pritsep_nomer(
        pritsep_nomer_davlat=country_code_pritsep,
        truck_pritsep_nomer=pritsep_nomer
    )

    update.message.reply_text(ADMIN_USER[lang][14])
    keyboard = [
        [KeyboardButton(ADMIN_BUTTONS[lang][5])],
        [KeyboardButton(ADMIN_BUTTONS[lang][6])],
        [KeyboardButton(ADMIN_BUTTONS[lang][7])]
    ]
    update.message.reply_text(
        start_user[lang][11],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ADMIN_MENU


def main():
    db.create_table()
    updater = Updater(
        token=TOKEN,
        use_context=True,
        request_kwargs={'read_timeout': 160, 'connect_timeout': 20}
    )
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("admin", admin),
        ],
        states={
            NAME: [CallbackQueryHandler(set_language, pattern="^lang_"),
                   MessageHandler(Filters.text & ~Filters.command, get_name)],
            PHONE: [MessageHandler(Filters.contact | Filters.text, get_phone)],
            LOCATION: [MessageHandler(Filters.location | Filters.text, get_location)],
            USER_TRUCK_KABINA: [CallbackQueryHandler(user_truck_kabina_nomer_save, pattern="^truck_")],
            USER_TRUCK_PRITSEP: [CallbackQueryHandler(user_pritsep_save, pattern="^pritsep_")],
            USER_TRUCK_KABINA_SELECT: [CallbackQueryHandler(user_pritsep_nomer, pattern="^kabina_")],
            USER_YONALISHI: [CallbackQueryHandler(yonalish_save, pattern="^yonalish_")],
            MAIN_MENU: [MessageHandler(Filters.text & ~Filters.command, menu_buttonslar)],

            USER_HARAJATLAR: [MessageHandler(Filters.text & ~Filters.command, user_kunlik_harajatlar)],

            USER_VALYUTA_OZIQ_OVQAT: [MessageHandler(Filters.text & ~Filters.command, save_oziq_valyuta)],
            USER_OZIQ_OVQAT: [MessageHandler(Filters.text & ~Filters.command, oziq_ovqat_rasxod)],
            OZIQ_OVQAT_CHEK: [MessageHandler(Filters.photo, oziq_ovqat_chek)],

            USER_TEL_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, telefon_valyuta_save)],
            USER_TELEFON: [MessageHandler(Filters.text & ~Filters.command, telefon_summa_save)],
            TELEFON_CHEK: [MessageHandler(Filters.photo, telefon_chek)],

            USER_STAYANKA_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, stayanka_valyuta_save)],
            USER_STAY_SUMMA: [MessageHandler(Filters.text & ~Filters.command, stayanka_summa_save)],
            STAYANKA_CHEK: [MessageHandler(Filters.photo, stayanka_chek)],

            USER_YOQIGI_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, yoqilgi_valyuta)],
            USER_YOQILGI_1L_NARX_SAVE: [MessageHandler(Filters.text & ~Filters.command, yoqilgi_1l_narx)],
            USER_YOQILGI_UMUMIY_HAJMI: [MessageHandler(Filters.text & ~Filters.command, yoqilgi_umumiy_hajmi)],
            YOQIGI_CHEK: [MessageHandler(Filters.photo, yoqilgi_chek)],

            USER_TEXNIK_XARAJATLAR: [MessageHandler(Filters.text & ~Filters.command, texnik_harajatlar)],
            USER_BALON_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, balon_valyuta_save)],
            USER_BALON_NARX_SAVE: [MessageHandler(Filters.text & ~Filters.command, balon_narxi_save)],
            BALON_CHEK: [MessageHandler(Filters.photo, balon_chek)],

            USER_MOTOR_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, motor_valyuta)],
            USER_MOTOR_NARX_SAVE: [MessageHandler(Filters.text & ~Filters.command, motor_narxi_save)],

            USER_ANTFRIS_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, anfris_valyuta)],
            USER_ANTFRIS_NARX_SAVE: [MessageHandler(Filters.text & ~Filters.command, antfris_narx_save)],
            ANTFRIS_CHEK: [MessageHandler(Filters.photo, antsfris_chek)],

            USER_AFTOL_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, aftol_valyuta)],
            USER_AFTOL_NARX_SAVE: [MessageHandler(Filters.text & ~Filters.command, aftol_narx_save)],
            AFTOL_CHEK: [MessageHandler(Filters.photo, aftol_chek)],

            SETTINGS_MENU: [CallbackQueryHandler(settings_menu_save, pattern="^lang_"),
                            MessageHandler(Filters.text & ~Filters.command, settings_menu)],

            USER_YANGI_YONALISHI: [MessageHandler(Filters.text & ~Filters.command, user_yangi_yonalish)],
            USER_TRANSPORTNI: [MessageHandler(Filters.text & ~Filters.command, Transportni_narx_save)],
            TRANSPORTNI_JOYLASHUVI: [MessageHandler(Filters.text & ~Filters.command, transpootrni_rasxod)],
            TRANSPORTNI_VALYUTA: [MessageHandler(Filters.text & ~Filters.command, transportni_valyuta)],
            YANGI_LOCATION: [MessageHandler(Filters.location & ~Filters.command, yangi_location)],

            ADMIN_LANG_STATE: [CallbackQueryHandler(admin_set_language, pattern="^lang_")],
            ADMIN_MENU: [CommandHandler("admin", admin_login),
                        MessageHandler(Filters.text & ~Filters.command, admin_select)],

            TRUCK_NAME: [MessageHandler(Filters.text & ~Filters.command, truck_name)],
            TRUCK_NAME_CATEGORY: [MessageHandler(Filters.text & ~Filters.command, truck_kabina_category)],
            PRODUCT_TRUCK_KABINA_DAVLAT: [CallbackQueryHandler(truck_kabina_davlat_nomer, pattern="^kabina_country_")],
            PRODUCT_TRUCK_KABINA_NOMERI: [
                MessageHandler(Filters.text & ~Filters.command, truck_kabina_davlat_nomer_save)],

            PRODUCT_TRUCK_PRITSEP_DAVLAT: [
                CallbackQueryHandler(truck_pritsep_davlat_nomer, pattern="^pritsep_country_")],
            PRODUCT_TRUCK_PRITSEP_NOMERI: [
                MessageHandler(Filters.text & ~Filters.command, truck_pritsep_davlat_nomer_save)]
        },
        fallbacks=[
            CommandHandler("start", start),
        ]
    )

    dp.add_handler(conv_handler, group=0)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, resume_router), group=1)
    dp.add_handler(CommandHandler("bind", bind_group))
    dp.add_handler(CommandHandler("gp", gp_bot))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
