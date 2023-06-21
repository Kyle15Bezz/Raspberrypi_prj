import pygame
from email_new import snd_email
import drivers

input_string = ""
display = drivers.Lcd()


def update_lcd():
    """
    Update the LCD display with the current input string.
    """
    display.lcd_clear()
    snd_row = ''
    first_row = input_string

    if len(input_string) > 16:
        first_row = input_string[:16]
        snd_row = input_string[16:]
    display.lcd_display_string(first_row, 1)
    display.lcd_display_string(snd_row, 2)


def key_pressed(event):
    """
    Handle keypress events and update the input string accordingly.
    """
    global input_string
    if event.type == pygame.KEYDOWN:
        key = pygame.key.name(event.key)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if event.key == pygame.K_2:
                input_string += "@"
                key = ''
        elif event.key == pygame.K_BACKSPACE:
            input_string = input_string[:-1]

        if key == "return":
            pygame.quit()
            return input_string
        elif len(key) == 1:
            if key == "space":
                key = " "

            input_string += key
        print(input_string)
        update_lcd()


def runn(weather, humidity, temp, wind, icon, option):
    """
    Run the main loop for capturing user input and sending an email.
    """
    pygame.init()

    pygame.display.set_mode((100, 100))

    # Block unwanted events
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.ACTIVEEVENT)
    pygame.event.set_blocked(pygame.VIDEORESIZE)
    pygame.event.set_blocked(pygame.VIDEOEXPOSE)
    pygame.event.set_blocked(pygame.USEREVENT)

    # Allow keydown events
    pygame.event.set_allowed(pygame.KEYDOWN)

    try:
        while True:
            try:
                for event in pygame.event.get():
                    key_pressed(event)
            except:
                snd_email(weather, humidity, temp, wind, icon, option, input_string)
                return

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
