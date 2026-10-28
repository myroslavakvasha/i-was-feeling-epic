# Single source of truth for subgenres.
# (slug, name, description)
#   slug        - stable ID used in code, DB lookups and the Ollama answer
#   name        - display name shown in the UI
#   description - ONLY used in the Ollama prompt (not stored in the DB)

SUBGENRES: list[tuple[str, str, str]] = [
    # --- Killers & stalkers ---
    ("slasher", "Slasher",
     "A masked or hidden killer stalks and murders a group of people one by one, often teens."),
    ("serial-killer", "Serial Killer",
     "The story centers on a serial killer or on someone hunting one, treated with horror tone rather than as a plain crime procedural."),
    ("home-invasion", "Home Invasion",
     "Strangers break into a home and terrorize the people inside; the threat is human and the setting is a house."),
    ("stalker-obsession", "Stalker / Obsession",
     "Someone is relentlessly followed, watched or obsessed over by a person who becomes a growing danger."),

    # --- Supernatural ---
    ("haunted-house", "Haunted House",
     "A home or building is haunted by ghosts or spirits that torment the people who live or stay there."),
    ("ghost-story", "Ghost Story",
     "A ghost or vengeful spirit haunts a person, family or community, tied to a past death or injustice."),
    ("demonic-possession", "Demonic Possession / Exorcism",
     "A demon or evil entity possesses a person, often leading to an exorcism or religious confrontation."),
    ("occult-witchcraft", "Occult / Witchcraft",
     "Witches, curses, black magic, satanic rituals or occult forces drive the threat."),
    ("cursed-object", "Cursed Object",
     "A haunted, cursed or evil object (doll, mirror, tape, house item) brings doom to whoever owns it."),
    ("urban-legend", "Urban Legend",
     "Based on a folk tale, local legend, chain-letter curse or internet myth that turns real."),
    ("paranormal-investigation", "Paranormal Investigation",
     "Investigators, mediums or researchers explore reported hauntings and uncover something real."),

    # --- Creatures ---
    ("creature-feature", "Creature Feature",
     "A monstrous creature, mutant or unknown beast terrorizes people."),
    ("natural-horror", "Animal Attack / Nature Strikes Back",
     "Ordinary or mutated animals, or nature itself (sharks, snakes, bears, insects), attack humans."),
    ("zombie", "Zombie",
     "The dead return to life or an infection turns people into mindless, hungry creatures."),
    ("vampire", "Vampire",
     "Vampires or blood-drinking undead are the main threat or central characters."),
    ("werewolf", "Werewolf",
     "People transform into wolf-like monsters, usually tied to a curse or the full moon."),

    # --- Mind & body ---
    ("psychological", "Psychological Horror",
     "Fear comes from a character's mind: paranoia, unreliable reality, madness, trauma or gaslighting."),
    ("body-horror", "Body Horror",
     "The human body is mutated, infected, mutilated or transformed in disturbing ways."),
    ("creepy-kids", "Creepy Kids",
     "Children are the source of the horror, or disturbing events center on a strange or sinister child."),

    # --- Style / format ---
    ("found-footage", "Found Footage",
     "Presented as discovered or amateur recordings (camcorder, phone, security camera, mockumentary), shot in first person."),
    ("screenlife", "Screenlife / Tech Horror",
     "Told through screens, apps, video calls or technology; or the horror comes from devices, AI or the internet."),
    ("anthology", "Anthology",
     "Made of several separate short horror stories, sometimes linked by a framing story."),
    ("slow-burn", "Slow Burn",
     "Patient, atmospheric pacing with dread that builds gradually instead of constant scares."),
    ("elevated-horror", "Elevated Horror",
     "Arthouse-leaning horror using the genre to explore grief, trauma, family or social themes, with strong craft and symbolism."),
    ("gothic", "Gothic",
     "Brooding atmosphere, old mansions, decay, romance and dark secrets, often period-set."),
    ("splatter-extreme", "Splatter / Extreme",
     "Graphic gore, torture or brutality is the main focus and the main source of shock."),

    # --- Settings & situations ---
    ("survival-horror", "Survival Horror",
     "A person or group fights to survive in isolation (cabin, woods, island, ship, trapped space) against a deadly threat."),
    ("folk-horror", "Folk Horror",
     "Rural isolation, pagan traditions, old beliefs and sinister communities or rituals."),
    ("cult", "Cult",
     "A cult or secret society, its leader or its rituals threaten the protagonists."),
    ("backwoods", "Backwoods / Rural Menace",
     "City people are hunted or terrorized by hostile locals or inbred families in remote rural areas."),
    ("asylum-medical", "Asylum / Medical Horror",
     "Hospitals, asylums, clinics, experiments or medical procedures are the setting of the horror."),
    ("apocalyptic", "Apocalyptic / Post-Apocalyptic",
     "The world has ended or is ending, and survivors face monsters, infection, or collapsing society."),
    ("revenge-horror", "Revenge Horror",
     "A victim or avenger turns violently on the people who wronged them."),
    ("holiday-horror", "Holiday Horror",
     "Horror set around a holiday such as Halloween, Christmas or Easter, with the holiday central to the story."),

    # --- Hybrids ---
    ("horror-comedy", "Horror Comedy",
     "Intentionally funny horror that mixes scares with comedy or satire."),
    ("sci-fi-horror", "Sci-Fi Horror",
     "Horror in a science-fiction setting: aliens, space, experiments gone wrong, or advanced technology."),
    ("cosmic-horror", "Cosmic Horror",
     "Humans face vast, incomprehensible forces or entities; themes of insignificance, madness and the unknowable."),
]

SUBGENRE_SLUGS: set[str] = {slug for slug, _, _ in SUBGENRES}

# Fail loudly at import time if a slug is duplicated.
assert len(SUBGENRE_SLUGS) == len(SUBGENRES), "duplicate slug in SUBGENRES"


def subgenres_for_prompt() -> str:
    return "\n".join(f"- {slug}: {description}" for slug, _, description in SUBGENRES)