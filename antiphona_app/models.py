"""All the models are here."""

from django.db import models


class Anno(models.Model):
    """
    This is the cycle for sundays: A, B, C
    and for weekdays: I, II
    """
    name = models.CharField(max_length=2)

    def __str__(self):
        return f"Anno {self.name}"


class AntiphonaType(models.Model):
    """
    Introito, Offertorium, Communio.
    Also some special antiphonas for special masses.
    """
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"Antiphona ad {self.name}"


class MissaType(models.Model):
    """
    This is the mass type, like Dominica or Feria.
    It's also important because it will allow us to
    have "custom" mass types in which there are different
    kinds of antiphonas, like ad Vigiliam Paschalem where
    you have antiphonas ad Liturgiam Baptismalem, etc.
    """
    name = models.CharField(max_length=40)
    antiphona_types = models.ManyToManyField(AntiphonaType, through="MissaType_AntiphonaType")

    @classmethod
    def get_default_missa_type(cls):
        """Returns the default missa type in case anyone deleted a reference."""
        return cls.objects.get_or_create(name="Dominica")[0]

    def __str__(self):
        return self.name


class MissaType_AntiphonaType(models.Model):
    """Connects the MissaType with the AntiphonaType adding an order to show"""
    missa_type = models.ForeignKey(MissaType, models.CASCADE)
    antiphona_type = models.ForeignKey(AntiphonaType, models.CASCADE)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.missa_type} - ({self.order}) {self.antiphona_type}"


class Missa(models.Model):
    """This is the celebration itself."""
    name = models.CharField(max_length=40)
    missa_type = models.ForeignKey(
        MissaType,
        on_delete=models.SET_DEFAULT,
        default=MissaType.get_default_missa_type,
    )
    antiphonae = models.ManyToManyField('Antiphona', through='Antiphona_Missa')

    def __str__(self):
        return self.name


class Antiphona(models.Model):
    """
    This is the antiphona itself. Should be in latin
    and will handle translation somewhere else.
    """
    name = models.CharField(max_length=120)
    text = models.CharField(max_length=300)
    missae = models.ManyToManyField(Missa, through='Antiphona_Missa')

    def __str__(self):
        return self.name


class Documentum(models.Model):
    """
    This is where the antiphona comes from:
    Missale Romanum, Graduale Romanum or Graduale Simplex.
    """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Antiphona_Missa(models.Model):
    """
    Connects an Antiphona with a Missa.

    Attributes:
        * Anno and Evangelium are meant to be used when for example the
            Graduale says 'Anno A' or 'Quando legitur Evangelium de ...'.
        * Antiphona Type is Introito, Offertorium, Communio, etc.
        * Documentum is which source this came from (MR, GR, GS)
        * Psalm is a string with the versicles for this antiphona.
    """
    antiphona = models.ForeignKey(Antiphona, models.CASCADE)
    missa = models.ForeignKey(Missa, models.CASCADE)

    anno = models.ForeignKey(Anno, models.PROTECT, null=True, blank=True)
    evangelium = models.CharField(max_length=80, null=True, blank=True)
    antiphona_type = models.ForeignKey(AntiphonaType, models.PROTECT)
    documentum = models.ForeignKey(Documentum, models.PROTECT)
    psalm = models.CharField(max_length=80, blank=True)
    alt_psalm = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return f"{self.missa} - {self.antiphona}"


class Suggestion(models.Model):
    """A single suggestion for an antiphona + psalm."""
    song_name = models.CharField(max_length=40)
    author = models.CharField(max_length=40, blank=True)
    audio_link = models.URLField(max_length=120, blank=True)
    sheet_link = models.URLField(max_length=120, blank=True)
    similarity = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    antiphona_missa = models.ForeignKey(Antiphona_Missa, models.CASCADE)

    def __str__(self):
        return f"Suggestion: {self.song_name} - {self.author}, for {self.antiphona_missa}"
