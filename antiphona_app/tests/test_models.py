"""Tests for the Models."""

from django.test import TestCase

from antiphona_app.models import (
    Antiphona,
    Antiphona_Missa,
    AntiphonaType,
    Documentum,
    Missa,
    MissaType,
)


class AntiphonaTests(TestCase):
    """Tests for the Antiphona class"""

    def setUp(self):
        # types gets
        self.missa_type = MissaType.objects.get(name="Dominica")
        self.antiphona_type = AntiphonaType.objects.get(name='Introito')
        self.documentum = Documentum.objects.get(name='Graduale Romanum')

        # real creations
        self.antiphona_name = "Ad te levavi"
        self.antiphona_text = (
            "Ad te levavi animam meam : "
            "Deus meus in te confido, non erubescam : "
            "neque irrideant me inimicimei : "
            "etenim universi qui te exspectant, non confundentur."
        )
        self.pre_antiphona = Antiphona.objects.create(
            name=self.antiphona_name,
            text=self.antiphona_text,
        )
        self.missa = Missa.objects.create(
            name="Dominica I Adventus",
            missae_type=self.missa_type,
        )
        self.psalm = "Ps. 24, 4"
        self.pre_antiphona_missa = Antiphona_Missa.objects.create(
            antiphona=self.pre_antiphona,
            missa=self.missa,
            anno=None,
            evangelium=None,
            antiphona_type=self.antiphona_type,
            documentum=self.documentum,
            psalm=self.psalm,
            alt_psalm="",
        )

        # get after creation
        self.antiphona = Antiphona.objects.get(id=self.pre_antiphona.id)
        self.antiphona_missa = Antiphona_Missa.objects.get(id=self.pre_antiphona_missa.id)

    def test_saved_name(self):
        """Name saved properly"""
        self.assertEqual(self.antiphona.name, self.antiphona_name)

    def test_saved_text(self):
        """Text saved properly"""
        self.assertEqual(self.antiphona.text, self.antiphona_text)

    def test_saved_missa(self):
        """Missa saved properly"""
        self.assertIn(self.missa, self.antiphona.missae.all())

    def test_saved_antiphona_in_connection(self):
        """Antiphona saved properly"""
        self.assertEqual(self.antiphona_missa.antiphona, self.antiphona)

    def test_saved_missa_in_connection(self):
        """Missa saved properly"""
        self.assertEqual(self.antiphona_missa.missa, self.missa)

    def test_saved_anno_in_connection(self):
        """Anno saved properly"""
        self.assertIsNone(self.antiphona_missa.anno)

    def test_saved_evangelium_in_connection(self):
        """Evangelium saved properly"""
        self.assertIsNone(self.antiphona_missa.evangelium)

    def test_saved_antiphona_type_in_connection(self):
        """Antiphona Type saved properly"""
        self.assertEqual(self.antiphona_missa.antiphona_type, self.antiphona_type)

    def test_saved_documentum_in_connection(self):
        """Documentum saved properly"""
        self.assertEqual(self.antiphona_missa.documentum, self.documentum)

    def test_saved_psalm_in_connection(self):
        """Psalm saved properly"""
        self.assertEqual(self.antiphona_missa.psalm, self.psalm)

    def test_saved_alt_psalm_in_connection(self):
        """Alt Psalm saved properly"""
        self.assertEqual(self.antiphona_missa.alt_psalm, "")
