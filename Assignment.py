#Name: Alexis 'Alex' Falourd , Student No. A00027313

#Title: Music Playlist and MP3 player
# Description: 

#My code shows a small demo of my music playlist. It features a scrollable song menu, when clicked it displays an mp3 interface where it shows the album cover, title, and waveform of the song of your choice. The user can use keyboard shortcuts like ‘Q’ to go to the previous track, ‘E’ to go to the next track, and ‘P’ to return to the menu.

#I’m most proud of the UI of my code. It’s a small detail but I had it where when you hover over the album cover at the main menu , the album cover enlarges a little to show some form of feedback.

# Interaction Instructions:
# Scroll to browse through songs
# Click an album cover to play the song
# Q = Previous track
# E = Next track
# P = Return to main menu
# SPACE = Pause / Resume

# Technical Requirements Breakdown:
# Lists: Used to store song dictionaries containing title, file, and cover
# Dictionaries: Each song is a dictionary with keys 'title', 'file', and 'cover'
# Loops: Used to draw menu items, draw waveform points, and load images
# Conditionals: You can control hover effects, play/pause logic, menu switching, and bounds for scrolling
# Complex logic: Hover detection makes album covers bigger, waveform visualization has real-time audio, scroll_offset manages menu scrolling
# Testing/Refinement: I adjusted the hover scaling, at first I made it too big by having it as 250 but changed it to 175, and made sure key controls respond correctly


import py5
from processing.sound import SoundFile, Waveform, Amplitude

# Songs
songs = [
    {"title": "Pierce the Veil - Bulletproof Love", "file": "BulletproofLove.mp3", "cover": "SelfishMachines.jpg"},
    {"title": "Pierce the Veil - I'm Low On Gas And You Need A Jacket", "file": "ImLowOnGasAndYouNeedAJacket.mp3", "cover": "CollideWithTheSky.jpg"},
    {"title": "Pierce the Veil - King For A Day", "file": "KingForADay.mp3", "cover": "CollideWithTheSky.jpg"},
    {"title": "Pierce the Veil - Circles", "file": "Circles.mp3", "cover": "Misadventures.jpg"},
    {"title": "Pierce the Veil - Emergency Contact", "file": "EmergencyContact.mp3", "cover": "JawsOfLife.jpg"},
    {"title": "Pierce the Veil - So Far So Fake", "file": "SoFarSoFake.mp3", "cover": "JawsOfLife.jpg"},
    {"title": "BAD OMENS - ARTIFICIAL SUICIDE", "file": "ARTIFICIALSUICIDE.mp3", "cover": "TheDeathOfPeaceOfMind.jpg"},
    {"title": "BAD OMENS X HEALTH X SWARM - THE DRAIN", "file": "THEDRAIN.mp3", "cover": "ConcreteJungleOST.jpg"},
    {"title": "Bilmuri - THE END", "file": "THEEND.mp3", "cover": "AmericanMotorSports.jpg"},
    {"title": "Suilen - Magnolia", "file": "Magnolia.mp3", "cover": "Hellsing.jpg"},
]

# Current song 
current_index = -1
soundfile = None
waveform = None
amplitude = None
paused = False

# Menu 
cover_size = 150
hover_size = 175
spacing = 50
scroll_offset = 0
album_covers = []

# loads the album covers
def setup():
    global album_covers
    py5.size(800, 800)
    py5.rect_mode(py5.CENTER)
    py5.text_align(py5.LEFT, py5.CENTER)

    for song in songs:
        try:
            img = py5.load_image(song['cover'])
            album_covers.append(img)
        except:
            album_covers.append(None)

# Main Menu draw loop
def draw():
    py5.background(0)
    if current_index == -1:
        draw_menu()
    else:
        draw_player()

# Text size and aligning
def set_text_style(size=16, align_x=py5.LEFT, align_y=py5.CENTER):
    py5.text_size(size)
    py5.text_align(align_x, align_y)

# Draws the scrollable menu with all the albums and artist/song name on display
def draw_menu():
    set_text_style()
    py5.fill(255)

    y_pos = spacing - scroll_offset + cover_size / 2
    x_pos = spacing + cover_size / 2

    for i, song in enumerate(songs):
        img = album_covers[i]
        img_size = cover_size

        # Makes the album cover bigger when the mouse is over it
        if img and (x_pos - hover_size/2 <= py5.mouse_x <= x_pos + hover_size/2 and
                    y_pos - hover_size/2 <= py5.mouse_y <= y_pos + hover_size/2):
            img_size = hover_size

        if i == current_index:
            py5.stroke(200, 200, 255)
            py5.stroke_weight(3)
            py5.rect(x_pos, y_pos, img_size+10, img_size+10)
            py5.no_stroke()

        if img:
            py5.image(img, x_pos - img_size/2, y_pos - img_size/2, img_size, img_size)

        py5.text(song['title'], x_pos + img_size/2 + 20, y_pos)
        y_pos += cover_size + spacing

# Click to play
def mouse_pressed():
    global current_index, paused
    if current_index == -1:
        y_pos = spacing - scroll_offset + cover_size / 2
        for i, img in enumerate(album_covers):
            if img and (y_pos - hover_size/2 <= py5.mouse_y <= y_pos + hover_size/2): # This enlarges the album when you hover over it with your mouse
                current_index = i
                paused = False
                load_song(current_index)
                break
            y_pos += cover_size + spacing

# Scroll menu (use mouse wheel)
def mouse_wheel(event):
    global scroll_offset
    if current_index == -1:
        scroll_offset += event.get_count() * 30
        scroll_offset = max(0, scroll_offset)
        max_scroll = max(0, len(songs)*(cover_size + spacing) - py5.height + spacing)
        scroll_offset = min(scroll_offset, max_scroll)

#Keys to press (E = next song, Q = previous song, P = menu)
def key_pressed():
    global current_index, paused
    if current_index != -1 and soundfile:
        if py5.key == ' ':
            paused = not paused
            soundfile.amp(0 if paused else 1)
        elif py5.key.lower() == 'e':
            next_song()
        elif py5.key.lower() == 'q':
            previous_song()
        elif py5.key.lower() == 'p':
            soundfile.stop()
            current_index = -1
            paused = False

# Load and play a song
def load_song(index):
    global soundfile, amplitude, waveform, paused
    if soundfile:
        soundfile.stop()
    paused = False
    file_path = songs[index]['file']
    soundfile = SoundFile(py5.get_current_sketch(), file_path)
    soundfile.play()
    soundfile.amp(1)

    amplitude = Amplitude(py5.get_current_sketch())
    amplitude.input(soundfile)
    waveform = Waveform(py5.get_current_sketch(), 512)
    waveform.input(soundfile)

# Play next song
def next_song():
    global current_index
    current_index = (current_index + 1) % len(songs)
    load_song(current_index)

# Play previous song
def previous_song():
    global current_index
    current_index = (current_index - 1) % len(songs)
    load_song(current_index)

# Current songs waveform
def draw_player():
    py5.background(0)

    cover_img = album_covers[current_index]
    cover_w = py5.width * 0.4
    cover_x = py5.width/2 - cover_w/2
    cover_y = 100

    if cover_img:
        py5.image(cover_img, cover_x, cover_y, cover_w, cover_w)

    # Song title
    set_text_style(24, py5.CENTER, py5.CENTER)
    py5.fill(255)
    py5.text(songs[current_index]['title'], py5.width/2, 60)

    # Waveform
    if waveform and amplitude and soundfile:
        py5.stroke(210,10,46)
        py5.stroke_weight(2)
        top = cover_y + cover_w + 50
        bottom = py5.height - 100
        h = bottom - top
        scale = 0.3
        if not paused:
            waveform.analyze()
        for i, val in enumerate(waveform.data):
            x = py5.remap(i, 0, len(waveform.data), 0, py5.width)
            y = top + h/2 + val*h/2*scale
            py5.point(x, y)

    # Controls text
    set_text_style(16, py5.CENTER, py5.CENTER)
    py5.fill(255)
    py5.text("SPACE = Play/Pause   |   E = Next Song   |   Q = Previous Song   |   P = Menu",
             py5.width/2, py5.height - 40)

py5.run_sketch()