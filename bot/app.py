# from booking.booking import Booking

# with Booking() as bot:
#     bot.land_first_page()
#     bot.change_currency(currency='USD')
#     bot.select_place(place="Seychellerna", result_option=1)
#     bot.select_date()
#     bot.submit()

from tinder.tinder import Tinder

with Tinder() as bot:
    bot.land_first_page()
    bot.logIn()
    bot.loginButton()
    bot.loginFacebook()
    bot.startPage()
    bot.swipeClassifier(swipes=10)
