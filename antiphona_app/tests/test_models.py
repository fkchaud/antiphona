"""Tests for the Models."""

from parameterized import parameterized

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
            missa_type=self.missa_type,
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


class MissaTests(TestCase):
    """Tests for the Missa class"""

    def setUp(self):
        # basic types and names
        self.missa_type = MissaType.objects.get(name="Dominica")
        self.antiphona_type_names = ['Introito', 'Offertorium', 'Communio']
        self.antiphona_type = AntiphonaType.objects.get(name='Introito')
        self.documentum = Documentum.objects.get(name='Graduale Romanum')

        # real creations
        self.antiphona_attributes = {
            "name": "Ad te levavi",
            "text": (
                "Ad te levavi animam meam : "
                "Deus meus in te confido, non erubescam : "
                "neque irrideant me inimicimei : "
                "etenim universi qui te exspectant, non confundentur."
            ),
        }
        self.antiphona = Antiphona.objects.create(**self.antiphona_attributes)
        self.missa_attributes = {
            "name": "Dominica I Adventus",
            "missa_type": self.missa_type,
        }
        self.pre_missa = Missa.objects.create(**self.missa_attributes)
        self.antiphona_missa_attributes = {
            "antiphona": self.antiphona,
            "missa": self.pre_missa,
            "anno": None,
            "evangelium": None,
            "antiphona_type": self.antiphona_type,
            "documentum": self.documentum,
            "psalm": "Ps. 24, 4",
            "alt_psalm": "",

        }
        self.pre_antiphona_missa = Antiphona_Missa.objects.create(**self.antiphona_missa_attributes)

        # get after creation
        self.missa = Missa.objects.get(id=self.pre_missa.id)
        self.antiphona_missa = self.missa.antiphona_missa_set.first()

    def test_saved_missa_name(self):
        """Missa name saved properly"""
        self.assertEqual(self.missa.name, self.missa_attributes["name"])

    def test_saved_missa_type(self):
        """Missa type saved properly"""
        self.assertEqual(self.missa.missa_type, self.missa_type)

    def test_saved_antiphona_types(self):
        """Missa related antiphona types saved properly"""
        self.assertEqual(
            [at.name for at in self.missa.missa_type.antiphona_types.all()],
            self.antiphona_type_names,
        )

    def test_saved_antiphonae_list(self):
        """Missa antiphonae list saved properly"""
        self.assertEqual(list(self.missa.antiphonae.all()), [self.antiphona])

    def test_saved_antiphona_missa(self):
        """Antiphona_Missa saved properly"""
        self.assertEqual(self.antiphona_missa, self.pre_antiphona_missa)

    @parameterized.expand([
        ("antiphona",),
        ("missa",),
        ("anno",),
        ("evangelium",),
        ("antiphona_type",),
        ("documentum",),
        ("psalm",),
        ("alt_psalm",),
    ])
    def test_saved_antiphona_missa_attributes(self, attribute_name):
        """Antiphona_Missa attributes saved properly"""
        self.assertEqual(
            getattr(self.antiphona_missa, attribute_name),
            self.antiphona_missa_attributes[attribute_name],
        )
