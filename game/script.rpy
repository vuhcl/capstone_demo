# The script of the game goes in this file.
init python:
    config.menu_include_disabled = True
    config.side_image_only_not_showing = True

    class CharacterStats(BaseStatsObject):
        """
        Class to store characters' relationship values
        (Unused for now)
        """
        @property
        def connection(self):
            value = self.__dict__['connection']

            if not (0 <= value <= 1):
                value = max( 0, min( 1, value ) )
                self.connection = value

            return self.__dict__['connection']

    def show_state(st, at):
        """Function to return text object with the current state"""
        return Text("State: {0!s}".format(current_state)), None

    def adjust_contrast(st, at, img):
        """Adjust contrast of a given image based on a given state"""
        # c > 0, with values in (0.0 , 1.0) decreasing contrast,
        # and values > 1.0 increasing contrast.
        # We transform the state value so that the image would have
        # decreased contrast when the state is depressed (-2 or -1)
        # and increased contrast when the state is manic (2 or 1)
        c = current_state/4. + 1
        return im.MatrixColor(img, im.matrix.contrast(c)), None

    # Initialize variables
    current_state, next_state = 0, 0
    white_arrow = im.Scale("arrow.png", 80, 40)
    arrow_flip = im.Flip(white_arrow, horizontal=True)

    skip = True # Whether or not to skip through the days
    days = 0 # How many days have passed without state change
    first = True # Flag to show explanation the first time we play through a day
    go = True # Flag to mark whether the player went to class or not
    change = False # Flag to mark a change in state
    party = False # Flag to mark whether the player went to the party or not
    p_name = "Me" # Player's name

    style.button['Skip'].background = "#333"

init:
    # Declare background images.
    # Class DynamicDisplayable is used to allow changes the background's contrast
    # based on the current state.
    image room = DynamicDisplayable(adjust_contrast, img='room_morning_light_off.jpg')
    image room_dusk_off = DynamicDisplayable(adjust_contrast, img='room_dusk_light_off.jpg')
    image room_evening_on = DynamicDisplayable(adjust_contrast, img='room_evening_light_on.jpg')
    image room_evening_off = DynamicDisplayable(adjust_contrast, img='room_evening_light_off.jpg')
    image school = DynamicDisplayable(adjust_contrast, img='noon01.jpg')
    image state = DynamicDisplayable(show_state)
    image gray = Frame(im.MatrixColor('Gray.png', im.matrix.opacity(0.9)))
    # Set up layered image for character, which allow
    # for easy change of expression and outfit.
    layeredimage finn_org:
        group base:
            attribute school:
                "Finn - re-8.png"
            attribute home:
                "Finn - re-6.png"

        group facial_expression:
            pos (700, 250)
            attribute smile default:
                "expression - smile.png"
            attribute surprised:
                "expression - surprise.png"
            attribute unsure:
                "expression - unsure.png"
    # Resize the layer image
    image finn = LayeredImageProxy("finn_org", Transform(zoom=0.25))
    # Make a smaller copy to use as side image, shown when an invisible character
    # has a dialogue line.
    image side finn = LayeredImageProxy("finn", Transform(zoom=0.7, crop=(0, 0, 362, 362), xoffset=-50))


# Declare characters used by this game.
define narrator = nvl_narrator # Narrator for NVL mode
define adv_narrator = Character(None, kind=adv) # Narrator for ADV mode
define f = Character("Finn", kind=adv, image="finn") # Declare Finn and attach corresponding image
define m = Character("[p_name]", kind=adv) # Player

default player = Patient() # Initialize simulation model
default menuset = set() # Variable used to store menu choices to exclude

# Screen to show the toggle button "Skip" on top-right corner
screen skip_toggle():
    textbutton "Skip":
        align (0.99, 0.01)
        action ToggleVariable("skip")
        style style.button["Skip"]

# The game starts here.
label start:
    # Blinking arrow pointing at the current state text
    image blinking_arrow:
        xpos 130
        ypos 35
        alpha 1.0 # visible
        white_arrow
        0.75
        alpha 0.0 # invisible
        0.5
        repeat
    # Blinking arrow pointing at the "Skip" button
    image blinking_arrow_right:
        xpos 1170
        ypos 35
        alpha 1.0 # visible
        arrow_flip
        0.75
        alpha 0.0 # invisible
        0.5
        repeat
    scene room
    show screen skip_toggle
    show state at topleft onlayer screens
    window show

    """


    Welcome to the demo!

    As it is to demonstrate how the model and the front end comes together,
    certain features will not appear in or will differ from the final product.

    """

    show blinking_arrow onlayer overlay

    """
    For example, the top left corner shows the current state in the model.
    This is to show track the model, as well as to see how the state manifests
    in different aspects of the game.
    """

    "The current state is 0 because the game has not taken information from the model."

    "Let's do that and see how it affects the front end."

    $ current_state = player.get_state()
    window hide
    nvl clear
    hide blinking_arrow
    adv_narrator "[Click to continue]"
    window show
    """
    First, we can see that the state number shown has changed. The initial state
    randomly chosen at initiation of the scene (i.e., after the player choose
    'Start' at the main menu).
    """
    """
    Another change is in the background, whose contrast changes based on the
    current state, acting as a proxy to reflect the mental state.
    """
    nvl clear
    """
    Next, we will jump into some gameplay to see how the model's state
    influence gameplay.
    """
    show blinking_arrow_right onlayer overlay
    """
    This button on the right is used to toggle whether to skip through the days
    until the state changes (default is True). This helps you speed through this demo
    and see different states quicker.
    """
    hide blinking_arrow_right
    """



    One last note is that originally the timestep for updating the state
    in the model is 1 week. However, to speed things up, we would update
    the model every in-game day.

    Without further ado, let's start!
    """
    window hide
    nvl clear
    show gray

    adv_narrator "You are a junior in college living off campus with your two friends, Finn and Rianne. To cover the bills, you work part-time as a barista."
    adv_narrator "Most days of the week, you have classes until late afternoon, when you are free or start your 5-hour shift."
    # Allow player to name the protagonist
    python:
        p_name = renpy.input ("Oh, my bad. I forgot your name. Can you please remind me?",
                        "", length=20,)
        p_name.strip()
        if not p_name:
            p_name = "Me"
    hide gray
    jump start_day

    return

# The start of every day
label start_day:
    # Clear menuset
    $ menuset = 0
    scene room
    with fade
    # Events if the player went to the party the previous night
    if party:
        adv_narrator "You feel fatigued and dizzy. You try to recall what happened last night, but everything is a blur."
        m "Urgh... Probably had too many drinks last night."
        adv_narrator "You decided to sleep in and get some rest."
        $ party = False
    else:
        python:
            # Set up choices to exclude
            if current_state < 0:
                menuset = set(["Why go to class? Let's stay home and play games."])
            elif current_state > 0:
                menuset = set(["Relunctantly get out of bed and try to make yourself go to campus.",
                "You are unusually tired. Get some more sleep."])
            else:
                menuset = set(["Relunctantly get out of bed and try to make yourself go to campus.",
                "You are unusually tired. Get some more sleep.",
                "Why go to class? Let's stay home and play games."])
            # Randomize values
            chance = (abs(current_state) == 1 and renpy.random.random() < 0.5) or (current_state == 2 and renpy.random.random() < 0.2)
            success_p = renpy.random.random()
        # Announce the length of the previous episode if it just ended
        if change:
            adv_narrator "It took [days] days, but you finally feel different."
            $ days = 0
        # Show explanation on the first time
        if first:
            # Statement 'call' allows returning to this scene after the scene being called ends.
            call first from _call_first
        # Set up first menu choices and what to follow
        menu:
            set menuset
            adv_narrator "It's almost time for your class."
            # The if clause at the end is evaluated to decide
            # whether or do to enable the choice to the player
            "Leave early to have a few minutes spare time." if (current_state == 0 or chance):
                if current_state < 0:
                    if success_p > 0.1:
                        adv_narrator "You are unusually tired, but you try to be on time anyways."
                        jump school
                    else:
                        adv_narrator "You try to get out of bed, but end up just staring at the wall for hours."

                else:
                    if current_state > 0:
                        adv_narrator "You are a little distracted by the thought of fun activities, but you go to class anyways."
                    jump school

            "Relunctantly get out of bed and try to make yourself go to campus.":
                if current_state == -2:
                    if success_p > 0.7:
                        adv_narrator "Fighting against your lack of motivation, you drag yourself to class."
                        jump school
                    else:
                        adv_narrator "You hate yourself for it, and you don't know exactly why, but you just keep laying in bed."
                        adv_narrator "Time passes by, and before you know it, you drift away..."
                else:
                    jump school

            "You are unusually tired. Get some more sleep.":
                adv_narrator "You succumb to the mental and physical exhaustion."
            "Why go to class? Let's stay home and play games.":
                adv_narrator "Placeholder for line"
    # If the player reaches this point of the script, they didn't go to school.
    $ go = False
    adv_narrator "You missed your classes."
    # Go to next scene
    jump end_day

# Short scene to show the explanation on the first day
label first:
    window show
    """
    When the state is major depression or mania, choices that would be available
    at normal state are be disabled to portray the altered thought process.
    """
    """
    With minor depression or hypomania, these choices might still be available.
    However, a chosen action might still fail. The probability of success differs
    depending on the state as well.
    """
    """
    Moreover, the state will alter texts and events in the game, as will be shown
    later.
    """
    nvl clear
    window hide
    # Return to main scene
    return

# The scene if the player goes to school
label school:
    $ go = True
    scene school
    with fade
    adv_narrator "Walking through the campus, you hear someone calling your name..."
    f school smile "Hey, [p_name]!"
    show finn school smile
    f "What's up! Didn't see you this morning when I left home."
    m "Placeholder"
    if current_state < 0:
        show finn school unsure
        f "Are you okay? You sound tired."
    elif current_state > 0:
        show finn school surprised
        f "Wow you seem energized today. Did you drink too much coffee this morning or something?"
    if current_state == -2:
        adv_narrator "Not wanting to interact with anyone, you came up with an excuse to end the conversation and walk away."
        hide finn
        with dissolve
        adv_narrator "Finn seems a bit annoyed at you. You get even more overwhelmed at the thought that he would hate you now."
    else:
        f school smile "Well, I gotta go. See you later!"
        hide finn
        with dissolve
    jump end_day

# Last scene of a day
label end_day:
    scene room_dusk_off
    with fade
    # First case where the player went to school.
    if go:
        adv_narrator "You got back from school."
        if current_state < 0:
            adv_narrator "You are absolutely exhausted, but you are glad that you stuck it out through the day."
        menu:
            adv_narrator "There's quite some homework from class."
            "It's still early. Let's relax for a little bit.":
                if current_state != 0:
                    adv_narrator "You started a video on YouTube, telling yourself you only need half an hour to wind down."
                    scene room_evening_on
                    with fade
                    if current_state < 0:
                        adv_narrator "Yet, hours passed before you realize you're just absent-mindedly killing time."
                        if current_state == -1:
                            adv_narrator "You finally sit down to study, but didn't manage to do much before deciding to just go to sleep."

                    elif current_state == 1:
                        adv_narrator "Yet, half an hour turns into two hours before you finally get to your homework."
                    elif current_state == 2:
                        adv_narrator "Yet, you watch videos after videos."
                        adv_narrator "Rabbit holes led to rabbit holes, before you finally look at the clock and see that it's already early morning."
                else:
                    adv_narrator "Placeholder"
            "Let's sit down and get it done.":
                if current_state == -2:
                    adv_narrator "Mentally exhausted, you get your homework out but find yourself blankly staring at the pages."
                    scene room_evening_on
                    with fade
                    adv_narrator "Hours passed by, but all you could do was thumbing through the pages every now and then."
                elif current_state == -1:
                    scene room_evening_on
                    with fade
                    adv_narrator "Working through your homework slowly, you get a bit of work done before your bedtime."
                elif current_state == 1:
                    adv_narrator "You didn't do much because you keep making mistakes, but at least you're making progress."
                    scene room_evening_on
                    with fade
                    adv_narrator "Realizing it's already way past your bedtime, you go to sleep."
                elif current_state == 2:
                    scene room_evening_on
                    with fade
                    adv_narrator "Stumped by a hard problem, you get more and more irritated as you keep making mistakes."
                    adv_narrator "You decided to go online instead."
                    adv_narrator "Bumping into a post about a party nearby on social media, you decided to ditch the work and take off to the party."
                    $ party = True
                else:
                    adv_narrator "Placeholder"
    else: # Second case if the player did not go to school
        if current_state < 0:
            adv_narrator "When you finally wake up, it's already dusk outside."
            adv_narrator "You hear your phone going off a couple times, but can't be bothered enough to check it."
            adv_narrator "You could't even tell what you have done since waking up, but time slowly passes by..."
            scene room_evening_on
            with fade
            adv_narrator "You hear a knock on the door."
            m "Sorry, can't get the door right now. What's up?"
            f home unsure "Hey, it's Finn. you didn't go to class today."
            f home unsure "Tried to call and text but you never answered. You alright?"
            m "Sorry, just feeling a little sick today."
            m "Trying to go to sleep early and get some rest."
            f home unsure "Okay. Just let me know if anything's wrong."
            f home unsure "I'll see you tomorrow then."
        if current_state > 0:
            adv_narrator "When you finally get back to your room, it's already dusk outside."
            adv_narrator "You hear a knock on the door."
            adv_narrator "You opened the door. It's Finn."
            show finn home unsure
            f "Tried to call and text but you never answered. You alright?"
            m "Yeah, it's nothing much. My phone died and I forgot to charge it. Actually..."
            show gray
            with fade
            adv_narrator "You went on and on about your day with Finn."
            hide gray
            show finn home surprised
            f "Wow, you sure are talkative today."
            show finn home smile
            f home smile "Well, good to know you're okay. See you tomorrow then."
            hide finn
            with dissolve
            if current_state == 2:
                adv_narrator "Feeling bored, you fiddle around on your phone and play some games."

    scene room_evening_off
    with fade
    if current_state == -2:
        adv_narrator "Still feeling drained of energy, you crawl into bed."
        if go:
            adv_narrator "Oddly enough, your buzzing brain is too tired to work but too anxious to sleep."
        adv_narrator "You toss and turn for a few more hours before finally falling asleep."
    elif current_state == 2:
        if party:
            adv_narrator "You don't know what time it is or how much you drank, but you finally managed to get home."
        if go:
            adv_narrator "You go to bed, irritated that you haven't gotten any work done."
        else:
            adv_narrator "Before you know it, it's already early morning. You finally go to sleep."
    # Show the rest of the explanation on the first day
    # and mark explanation as shown.
    if first:
        $ first = False
        window show
        "That's the end of one in-game day in this demo."

        "Of course, the final product will be fleshed out more."
        "This would include music, more characters and events, i.e. a longer script."
        """
        On the technical side, interactions in the game would be updated to have
        impact on the player's mental health, relationship between characters,
        and long-term effect on the storyline (e.g.: consequence for skipping class
        too many times).
        """
        """
        I coded Python classes to support changing the relationship between characters,
        but currently they are unused.
        """
        nvl clear
        """


        Still, for now, you can keep going, have the model update its state,
        and see how different states affect the choices and outcome.
        """
        """
        You can also keep repeating or toggle \"Skip\" to False to see all possible
        paths in this demo.
        """
        window hide
        nvl clear
    # Update the model and get the next state
    python:
        next_state = player.get_new_state()
        days += 1
        if skip:
            while next_state == current_state:
                next_state = player.get_new_state()
                days += 1
        if next_state != current_state:
            change = True
        else:
            change = False
        current_state = next_state
    # Start a new day
    jump start_day
