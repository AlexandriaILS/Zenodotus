from django.db import models
from taggit.managers import TaggableManager


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BibliographicLevel(models.Model):
    MONOGRAPHIC_COMPONENT_PART = "a"
    SERIAL_COMPONENT_PART = "b"
    COLLECTION = "c"
    SUBUNIT = "d"
    INTEGRATING_RESOURCE = "i"
    MONOGRAPH_ITEM = "m"
    SERIAL = "s"

    LEVEL_OPTIONS = [
        (MONOGRAPHIC_COMPONENT_PART, "Monographic component part"),
        (SERIAL_COMPONENT_PART, "Serial component part"),
        (COLLECTION, "Collection"),
        (SUBUNIT, "Subunit"),
        (INTEGRATING_RESOURCE, "Integrating resource"),
        (MONOGRAPH_ITEM, "Monograph / Item"),
        (SERIAL, "Serial"),
    ]

    name = models.CharField(max_length=1, choices=LEVEL_OPTIONS)

    def __str__(self):
        return self.get_name_display()


class ItemTypeBase(models.Model):
    """
    Record type base.

    Used for organizing groups of materials if needed and for populating the
    leader of MARC records when exporting.
    """

    LANGUAGE_MATERIAL = "a"
    NOTATED_MUSIC = "c"
    MANUSCRIPT_NOTATED_MUSIC = "d"
    CARTOGRAPHIC_MATERIAL = "e"
    MANUSCRIPT_CARTOGRAPHIC_MATERIAL = "f"
    PROJECTED_MEDIUM = "g"
    NONMUSICAL_SOUND_RECORDING = "i"
    MUSICAL_SOUND_RECORDING = "j"
    TWO_DIMENSIONAL_NONPROJECTABLE_GRAPHIC = "k"
    COMPUTER_FILE = "m"
    KIT = "o"
    MIXED_MATERIALS = "p"
    THREE_DIMENSIONAL_ARTIFACT = "r"
    MANUSCRIPT_LANGUAGE_MATERIAL = "t"

    TYPE_OPTIONS = [
        (LANGUAGE_MATERIAL, "Language material"),
        (NOTATED_MUSIC, "Notated music"),
        (MANUSCRIPT_NOTATED_MUSIC, "Manuscript notated music"),
        (CARTOGRAPHIC_MATERIAL, "Cartographic material"),
        (MANUSCRIPT_CARTOGRAPHIC_MATERIAL, "Manuscript cartographic material"),
        (PROJECTED_MEDIUM, "Projected medium"),
        (NONMUSICAL_SOUND_RECORDING, "Nonmusical sound recording"),
        (MUSICAL_SOUND_RECORDING, "Musical sound recording"),
        (
            TWO_DIMENSIONAL_NONPROJECTABLE_GRAPHIC,
            "Two-dimensional nonprojectable graphic",
        ),
        (COMPUTER_FILE, "Computer file"),
        (KIT, "Kit"),
        (MIXED_MATERIALS, "Mixed materials"),
        (
            THREE_DIMENSIONAL_ARTIFACT,
            "Three dimensional artifact or naturally occuring object",
        ),
        (MANUSCRIPT_LANGUAGE_MATERIAL, "Manuscript language material"),
    ]

    name = models.CharField(max_length=1, choices=TYPE_OPTIONS)

    def __str__(self):
        return self.get_name_display()


class ItemType(models.Model):
    name = models.CharField(max_length=40)
    base = models.ForeignKey(ItemTypeBase, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Record(models.Model):
    """
    Information that should not change between different types of the same media.
    For example, an audiobook vs the original text.
    """

    # tag 245a
    title = models.CharField(max_length=26021)  # thanks, Yethindra
    # This may be multiple people in one string; it's a limitation of the MARC format.
    # Field 245c is used, as it always includes all authors.
    # This field may not have a relevant answer; for example, DVDs don't really have
    # an author. Filling this field out is encouraged, but therefore not required.
    authors = models.CharField(max_length=500, blank=True, null=True)

    # tag 245b
    subtitle = models.CharField(max_length=26021, blank=True, null=True)

    uniform_title = models.CharField(max_length=26021, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    # Is this part of a series, like a manga or something similar? Maybe a periodical?
    series = models.TextField(blank=True, null=True)

    subjects = models.ManyToManyField(
        Subject, blank=True, verbose_name="list of subjects"
    )

    tags = TaggableManager(blank=True)

    image = models.ImageField(blank=True, null=True)

    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, blank=True, null=True)

    bibliographic_level = models.ForeignKey(
        BibliographicLevel, on_delete=models.CASCADE, blank=True, null=True
    )

    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        val = f"{self.title}"
        if self.authors:
            val += f" | {self.authors}"
        if self.type:
            val += f" | {self.type.name}"
        return val
