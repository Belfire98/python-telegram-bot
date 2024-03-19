#!/usr/bin/env python

from telegram import PhotoSize, UserProfilePhotos
from tests.auxil.slots import mro_slots

class TestUserProfilePhotosBase:
    """
    A base class for testing UserProfilePhotos.
    """

    total_count: int = 2
    photos: tuple = (
        (
            PhotoSize("file_id1", "file_un_id1", 512, 512),
            PhotoSize("file_id2", "file_un_id1", 512, 512),
        ),
        (
            PhotoSize("file_id3", "file_un_id3", 512, 512),
            PhotoSize("file_id4", "file_un_id4", 512, 512),
        ),
    )

    def test_slot_behaviour(self):
        """
        Test that the instance has no extra slots.
        """
        inst = UserProfilePhotos(self.total_count, self.photos)
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_de_json(self) -> None:
        """
        Test that UserProfilePhotos can be deserialized from JSON.
        """
        json_dict = {"total_count": 2, "photos": [[y.to_dict() for y in x] for x in self.photos]}
        user_profile_photos = UserProfilePhotos.de_json(json_dict)
        assert user_profile_photos.api_kwargs == {}
        assert user_profile_photos.total_count == self.total_count
        assert isinstance(user_profile_photos.photos, tuple)
        for ix, x in enumerate(user_profile_photos.photos):
            assert isinstance(x, tuple)
            for iy, y in enumerate(x):
                assert isinstance(y, PhotoSize)

    def test_to_dict(self) -> None:
        """
        Test that UserProfilePhotos can be serialized to a dictionary.
        """
        user_profile_photos = UserProfilePhotos(self.total_count, self.photos)
        user_profile_photos_dict = user_profile_photos.to_dict()
        assert user_profile_photos_dict["total_count"] == user_profile_photos.total_count
        assert isinstance(user_profile_photos_dict["photos"], list)
        for ix, x in enumerate(user_profile_photos_dict["photos"]):
            assert isinstance(x, list)
            for iy, y in enumerate(x):
                assert isinstance(y, dict)
                assert y == user_profile_photos.photos[ix][iy].to_dict()

    def test_equality(self) -> None:
        """
        Test that UserProfilePhotos instances are compared correctly.
        """
        a = UserProfilePhotos(2, self.photos)
        b = UserProfilePhotos(2, self.photos)
        c = UserProfilePhotos(1, (self.photos[0],))
        d = PhotoSize("file_id1", "unique_id", 512, 512)

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)
